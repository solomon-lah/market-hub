from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import initialRegistrationForm,finalRegistrationForm,loginForm,upLoadForm,chatForm,editForm,editProfileForm,changeProfilePicForm
from .models import userTable,itemsTable, chatTable, communicatingPartyId
from django.utils import timezone
from django.db.models import Q
# Create your views here.

# homepage View
def home(request):
    return render(request, 'users/usersTemplate.html')
# signup View
def signUp(request):
   if request.method =='POST' and request.POST['form_owner'] == 'initialForm':
        initialForm = initialRegistrationForm(request.POST)
        if initialForm.is_valid():
           finalForm = finalRegistrationForm()
           email = request.POST['email']
           try:
               checkEmail = userTable.objects.get(email = email)
               context = {'initialForm': initialForm,'error':'This Email has already Registered'}
               return render(request,'users/signUp.html',context)
           except:
               c = ''
           finalForm['email'].initial = email
           finalForm['passcode'].initial = request.POST['passcode']
           return render(request,'users/signUp.html',{'finalForm':finalForm})
   elif request.method =='POST' and request.POST['form_owner'] == 'finalForm':
     finalForm = finalRegistrationForm(request.POST,request.FILES)
     if finalForm.is_valid():
         email = request.POST['email']
         passcode = request.POST['passcode']
         surname = request.POST['surname']
         firstname = request.POST['firstname']
         gender = request.POST['gender']
         phoneNumber = request.POST['phoneNumber']
         address = request.POST['address']
         image = request.FILES['image']
         insert = userTable(email = email,
                               passcode = passcode,
                               surname = surname,
                               firstname = firstname,
                               gender = gender,
                               phoneNumber = phoneNumber,
                               address = address,
                               img = image)
         insert.save()
         ''' line 48 to 51 function is to establish communication between admin and user,
         the saveintoComparty gives their chat identifier'''
         comParty = "admin "+ email
         saveIntoComParty = communicatingPartyId(parties = comParty)
         saveIntoComParty.save()
         request.session['user'] = email
         return redirect('hubPage')

     return render(request,'users/signUp.html',{'finalForm': finalForm})
   else:
       initialForm = initialRegistrationForm()
   return render(request,'users/signUp.html', {'initialForm': initialForm})

# login View
def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            passcode = request.POST['passcode']
            try:
                check = userTable.objects.get(email = email, passcode = passcode,status ='Allowed')
            except:
                context = {'form':form, 'error':'Invalid Login Credentials'}
                return render(request,'users/login.html',context)
            request.session['user'] = email
            return redirect('hubPage')
    else:
        form = loginForm()
    return render(request,'users/login.html',{'form': form})

# allUpload View
def hubHome(request):
    email = request.session.get('user')
    if  email == None :
        return redirect('loginPage')
    try:
        allUploads = itemsTable.objects.order_by('id')
        allUploads = allUploads.exclude(email = email)
    except:
        return render(request,'hub/hubTemplate.html')
    return render(request,'hub/hubTemplate.html',{'allUploads': allUploads})

# each upload View
def itemDetails(request, itemId):
    email = request.session.get('user')
    if email == None:
        return redirect('loginPage')
    try:
        confirmItem = itemsTable.objects.get(id = itemId)
    except:
        return redirect('hubPage')
    if confirmItem.email == email:
        return redirect('hubPage')
    getUploaderDetails = userTable.objects.get(email = confirmItem.email)
    comParty_1 = email + ' '+ confirmItem.email
    comParty_2 = confirmItem.email +' '+ email
    comId = ''
    try:
        check = communicatingPartyId.objects.get(Q(parties = comParty_1) | Q(parties = comParty_2))
        comId = check.id
    except:
        comId = communicatingPartyId(parties = comParty_1)
        comId.save()
        comId = comId.id

    context = {'itemDetails': confirmItem, 'uploaderDetails': getUploaderDetails,'comId':comId}
    return render(request,'hub/itemDetails.html', context)

# chat View
def chat(request,chatId):
    email = request.session.get('user')
    if email == None:
        return redirect('loginPage')
    chatIdentifier = ''
    lastChat = ''
    try:
        chatIdentifier = communicatingPartyId.objects.get(id = chatId, parties__contains = email)
    except:
        return redirect('hubPage')
    secondParty = chatIdentifier.parties
    secondParty = str.split(secondParty, ' ')
    chatHistory = chatTable.objects.filter(chatId = chatId)
    if len(chatHistory) != 0 :
        lastChat = chatHistory.last()
        if lastChat.receiver == email:
            lastChat.status = 'Seen'
            lastChat.save()
    if email != secondParty[0]:
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
            sender = email
            receiver = secondParty
            dateSent = timezone.now()
            if len(chatHistory) != 0 :
                lastChat.lastMessage = 'No'
                lastChat.save()
            insert = chatTable(chatId = chatId,
                                    message = message,
                                    img = img,
                                    sender = email,
                                    receiver = secondParty,
                                    dateSent = dateSent,
                                    status = 'Unseen',
                                    lastMessage = 'Yes')
            insert.save()
            return redirect('chatPage',chatId)
    else:
        form = chatForm()
    context ={'chatHistory':chatHistory, 'form' : form, 'owner': email}
    return render(request,'hub/chats.html', context)

# upload an item View
def upload(request):
    email = request.session.get('user')
    if email == None:
        return redirect('loginPage')
    if request.method=='POST':
        form = upLoadForm(request.POST,request.FILES)
        if form.is_valid():
            itemName = request.POST['itemName']
            itemPrice = request.POST['itemPrice']
            description = request.POST['description']
            category = request.POST['category']
            img_1 = request.FILES['img_1']
            img_2 = request.FILES['img_2']
            dateUploaded = timezone.now()
            insert = itemsTable(
                email = email,
                itemName = itemName,
                itemPrice = itemPrice,
                description = description,
                category = category,
                img_1 = img_1,
                img_2 = img_2,
                dateUploaded = dateUploaded
            )
            insert.save()
            form = upLoadForm()
            context ={'form': form, 'success':'Item Successfully Uploaded'}
            return render(request,'hub/upload.html',context)
    else:
        form = upLoadForm()
    return render(request,'hub/upload.html',{'form':form})

# all messages View
def allChats(request):
    email = request.session.get('user')
    if email == None:
        return redirect('loginPage')
    getMessages = chatTable.objects.filter((Q(receiver = email) | Q( sender = email)) & Q (lastMessage = 'Yes'))

    if len(getMessages) == 0:
        return render(request,'hub/messages.html',{'noMessage': 'Chat history Empty'})
    getMessages = getMessages.order_by('-id')
    objectReturned = []
    for f in getMessages:
        otherParty = ''
        if (f.sender == email):
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
    return render(request, 'hub/messages.html',{'allMessages': objectReturned,'owner':email})

# view for all upload by a user
def viewAllUploads(request):
    email = request.session.get('user')
    if email == None:
        return redirect('loginPage')
    allUploads = itemsTable.objects.filter(email = email)
    if len(allUploads) == 0:
        allUploads =''
    return render(request,'hub/allUploads.html',{'allUploads': allUploads})

# view individual item uploaded by a user
def individualItem(request,itemId):
    email = request.session.get('user')
    if email == None:
        return redirect('loginPage')
    try:
        item = itemsTable.objects.get(email = email, id = itemId)
    except:
        return redirect('allUploadsPage')
    return render(request,'hub/viewItem.html',{'item':item})

def updateItem(request,itemId):
    email = request.session.get('user')
    item = ''
    if email == None:
        return redirect('loginPage')
    try:
        item = itemsTable.objects.get(email = email, id = itemId)
    except:
        return redirect('allUploadsPage')
    if request.method == 'POST':
        form = editForm(request.POST)
        if form.is_valid():
            item.itemName = request.POST['itemName']
            item.itemPrice = request.POST['itemPrice']
            item.description = request.POST['description']
            item.save()
            return redirect('individualItemPage', itemId)
    else:
        form = editForm()
    form["itemName"].initial = item.itemName
    form["itemPrice"].initial = item.itemPrice
    form["description"].initial = item.description
    return render(request,'hub/editUpload.html',{'form':form})

def deleteItem(request,itemId):
    email = request.session.get('user')
    item = ''
    if email == None:
        return redirect('loginPage')
    try:
        item = itemsTable.objects.get(email = email, id = itemId)
    except:
        return redirect('allUploadsPage')
    if request.method == 'POST':
        item.delete()
        return redirect('allUploadsPage')
    return render(request,'hub/deleteItem.html',{'itemId':itemId})

# profile view
def profile(request):
    email = request.session.get('user')
    item = ''
    if email == None:
        return redirect('loginPage')
    details = userTable.objects.get(email = email)
    if request.method == 'POST':
        form = changeProfilePicForm(request.POST,request.FILES)
        details.img = request.FILES['img']
        details.save()
        form = changeProfilePicForm()
    else:
        form = changeProfilePicForm()
    return render(request,'hub/profile.html',{'details': details,'form':form})

#edit profile details view
def editProfile(request):
    email = request.session.get('user')
    item = ''
    if email == None:
        return redirect('loginPage')
    details = userTable.objects.get(email = email)
    if request.method == 'POST':
        form = editProfileForm(request.POST)
        if form.is_valid():
            details.surname = request.POST['surname']
            details.firstname = request.POST['firstname']
            details.phoneNumber = request.POST['phoneNumber']
            details.address = request.POST['address']
            details.save()
            return redirect('profilePage')
    else:
        form = editProfileForm()
        form["surname"].initial = details.surname
        form["firstname"].initial = details.firstname
        form["phoneNumber"].initial = details.phoneNumber
        form["address"].initial = details.address
    return render(request,'hub/editProfile.html',{'form': form})

#report view
def report(request):
    email = request.session.get('user')
    item = ''
    if email == None:
        return redirect('loginPage')
    lastChat = ''
    chatIdentifier = communicatingPartyId.objects.get(parties="admin "+ email)
    secondParty = "admin"
    chatHistory = chatTable.objects.filter(chatId=chatIdentifier.id)
    if request.method == 'POST':
        form = chatForm(request.POST, request.FILES)
        if form.is_valid():
            message = request.POST['message']
            img = ''
            try:
                img = request.FILES['img']
            except:
                img = img
            dateSent = timezone.now()
            if len(chatHistory) != 0:
                lastChat.lastMessage = 'No'
                lastChat.save()
            insert = chatTable(chatId=chatIdentifier.id,
                               message=message,
                               img=img,
                               sender=email,
                               receiver=secondParty,
                               dateSent=dateSent,
                               status='Unseen',
                               lastMessage='Yes')
            insert.save()
            return redirect ('chatPage',chatIdentifier.id)

    else:
        form = chatForm()

    return render(request, 'hub/chats.html',{'form': form})
# logout View
def logout(request):
    del request.session['user']
    return redirect('loginPage')
