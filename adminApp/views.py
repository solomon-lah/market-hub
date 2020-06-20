from django.utils import timezone

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import loginForm
from .models import adminTable
from users.models import userTable,chatTable,communicatingPartyId,itemsTable
from users.forms import chatForm
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            adminId = request.POST['adminId']
            passcode = request.POST['passcode']
            try:
                getAdmin = adminTable.objects.get(adminId = adminId, passcode = passcode )
            except:
                return render(request,'admin/login.html',{'form':form,'error':'Invalid login credentials'})
            request.session['admin'] = 'admin'
            return redirect('adminHomePage')
    else:
        form = loginForm()
    return render(request,'admin/login.html',{'form':form})
def homepage(request):
    checkAdmin = request.session.get('admin')
    if not checkAdmin:
        return redirect('adminLoginPage')
    return render(request,'admin/adminTemplate.html')

def allChats(request):
    checkAdmin = request.session.get('admin')
    if checkAdmin == None:
        return redirect('adminLoginPage')
    getMessages = chatTable.objects.filter((Q(receiver = checkAdmin) | Q( sender = checkAdmin)) & Q (lastMessage = 'Yes'))
    if len(getMessages) == 0:
        return render(request,'hub/messages.html',{'noMessage': 'Chat history Empty'})
    getMessages = getMessages.order_by('-id')
    objectReturned = []
    for f in getMessages:
        otherParty = ''
        if (f.sender == checkAdmin):
            otherParty = f.receiver
        else:
            otherParty = f.sender
        secondParty = otherParty
        if secondParty == 'admin':
            if len(f.message) > 100:
                f.message = f.message[0: 100]
            objectReturned.append({'chatId':f.chatId,'message': f.message,'otherParty': secondParty,'dateSent':f.dateSent
                                   ,'status':f.status,'image': '','names':'Hub Management team','sender': f.sender})
        else:

            otherParty = userTable.objects.get(email = otherParty)
            surname = otherParty.surname
            firstname = otherParty.firstname
            names = surname +' '+ firstname
            otherParty = otherParty.img
            if len(f.message) > 100:
                f.message = f.message[0: 100]
            objectReturned.append({'chatId':f.chatId,'message': f.message,'otherParty': secondParty,'dateSent':f.dateSent
                                   ,'status':f.status,'image': otherParty,'names':names,'sender': f.sender})
    return render(request, 'admin/reports.html',{'allMessages': objectReturned,'owner':checkAdmin})

# chat View
def chat(request,chatId):
    checkAdmin = request.session.get('admin')
    if checkAdmin == None:
        return redirect('adminLoginPage')
    chatIdentifier = ''
    lastChat = ''
    chatIdentifier = communicatingPartyId.objects.get(id = chatId, parties__contains = checkAdmin)
    secondParty = chatIdentifier.parties
    secondParty = str.split(secondParty, ' ')
    chatHistory = chatTable.objects.filter(chatId = chatId)
    if len(chatHistory) != 0 :
        lastChat = chatHistory.last()
        if lastChat.receiver == checkAdmin:
            lastChat.status = 'Seen'
            lastChat.save()
    if checkAdmin != secondParty[0]:
        secondParty = secondParty[0]
    else:
        secondParty = secondParty[1]
    if request.method == 'POST':
        form = chatForm(request.POST,request.FILES)
        if form.is_valid():
            message = request.POST['message']
            img = ''
            try :
                img = request.FILES['img']
            except :
                img = img
            dateSent = timezone.now()
            if len(chatHistory) != 0 :
                lastChat.lastMessage = 'No'
                lastChat.save()
            insert = chatTable(chatId = chatId,
                                    message = message,
                                    img = img,
                                    sender = checkAdmin,
                                    receiver = secondParty,
                                    dateSent = dateSent,
                                    status = 'Unseen',
                                    lastMessage = 'Yes')
            insert.save()
            return redirect('adminChatPage',chatId)
    else:
        form = chatForm()
    context ={'chatHistory':chatHistory, 'form' : form, 'owner': checkAdmin}
    return render(request,'admin/chats.html', context)

def allUploads(request):
        checkAdmin = request.session.get('admin')
        if not checkAdmin:
            return redirect('adminLoginPage')
        try:
            allUploads = itemsTable.objects.order_by('-id')
        except:
            return render(request, 'admin/allUploads.html')
        return render(request, 'admin/allUploads.html', {'allUploads': allUploads})

def itemDetails(request, itemId):
    admin = request.session.get('admin')
    if admin == None:
        return redirect('adminLoginPage')
    try:
        confirmItem = itemsTable.objects.get(id = itemId)
    except:
        return redirect('hubPage')

    getUploaderDetails = userTable.objects.get(email = confirmItem.email)
    context = {'itemDetails': confirmItem, 'uploaderDetails': getUploaderDetails}
    return render(request,'admin/itemDetails.html', context)
def allUsers(request):
    admin = request.session.get('admin')
    if admin == None:
        return redirect('adminLoginPage')
    try:
        allUsers = userTable.objects.all()
    except:
        return render(request,'admin/allUsers.html')
    return render(request,'admin/allUsers.html', {'userDetails': allUsers})

def suspendUser(request,userId):
    if request.method == 'POST':
        user = userTable.objects.get(id = userId)
        user.status = 'Blocked'
        user.save()
        return redirect('allUsersPage')
    return render(request,'admin/suspendUser.html')

def allSuspendedUser(request):
    admin = request.session.get('admin')
    if admin == None:
        return redirect('adminLoginPage')
    try:
        allUsers = userTable.objects.filter(status = 'Blocked')
    except:
        return render(request,'admin/allUsers.html')
    return render(request,'admin/allSuspendedUser.html', {'userDetails': allUsers})
def restoreUser(request,userId):
    if request.method == 'POST':
        user = userTable.objects.get(id = userId)
        user.status = 'Allowed'
        user.save()
        return redirect('allUsersPage')
    return render(request,'admin/suspendUser.html')
