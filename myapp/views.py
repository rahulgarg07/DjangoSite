from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
import datetime



from myapp.forms import RegisterForm, LoginForm, ForgotPassword, PasswordChangeForm, UserInfoForm, AboutMeInfoForm, \
    AddPostForm, AddCommentsForm, AddLikesForm
from myapp.models import User_info, Post_info, Topic, Relationship, Comments, Like
from django.contrib.auth import update_session_auth_hash



@login_required(login_url="/myapp/login/", redirect_field_name='')
def index(request):
    user_p = get_object_or_404(User_info, id=request.user.id)
    post_d = user_p.post_info_set.order_by('id')
    post_dt = Post_info.objects.all().distinct().order_by('-id')
    user_r = user_p.user_relationship.filter(to_user__rel_status=1)
    user_s = user_p.user_relationship.filter(to_user__rel_status=3)
    user_t = user_r|user_s
    return render(request, 'myapp/index.html', {'user_p': user_p,
                                                'post_dt': post_dt,
                                                'user_r': user_r,
                                                'post_d': post_d,
                                                'user_t': user_t
                                                })


@login_required(login_url="/myapp/login/", redirect_field_name='')
def my_prof(request):
    user = get_object_or_404(User_info, id=request.user.id)
    followers = user.related_to.all().count()-1
    following = user.user_relationship.all().count()-1
    post_data = user.post_info_set.order_by('id')
    user_r = user.user_relationship.filter(to_user__rel_status=1)
    post_dt = Post_info.objects.filter(post_user__to_user__rel_status=1).distinct()
    p_d = Relationship.objects.filter(rel_from_user__user_relationship__post_info=1)
    user_f = user.related_to.filter(from_user__rel_status=1)
    return render(request, 'myapp/myprofile.html', {'post_data': post_data,
                                                    'user': user,
                                                    'followers': followers,
                                                    'following': following,
                                                    'user_r': user_r,
                                                    'user_f': user_f,
                                                    'post_dt': post_dt,
                                                    'p_d': p_d
                                                    })


@login_required(login_url="/myapp/login/", redirect_field_name='')
def explore_viw(request):
    user = get_object_or_404(User_info, id=request.user.id)
    post_data = Post_info.objects.order_by('-id', '-post_publish_date', '-post_publish_time')
    return render(request, 'myapp/explore.html', {'user': user,
                                                  'post_data': post_data,
                                                  })



@login_required(login_url="/myapp/login/", redirect_field_name='')
def user_prof(request, id):
    user = get_object_or_404(User_info, id=request.user.id)
    user_prf = get_object_or_404(User_info, id=id)
    post_data = user_prf.post_info_set.order_by('-id', '-post_publish_date', '-post_publish_time')
    followers = user_prf.related_to.all().count()
    following = user_prf.user_relationship.all().count()
    followers_u = str(user.related_to.all())
    following_u = user.user_relationship.filter(to_user__rel_status=1)
    user_1 = User_info.objects.get(id=request.user.id)
    user_2 = user_prf
    if request.method == 'POST':
        if 'add_rel' in request.POST:
            Relationship.objects.get_or_create(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            )
            return render(request, 'myapp/userprofile.html', {'user_prf': user_prf,
                                                      'user': user,
                                                      'followers': followers,
                                                      'following': following,
                                                      'post_data': post_data,
                                                      'following_u': following_u,
                                                      'followers_u': followers_u})
        if 'del_rel' in request.POST:
            Relationship.objects.filter(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            ).delete()
            return render(request, 'myapp/userprofile.html', {'user_prf': user_prf,
                                                      'user': user,
                                                      'followers': followers,
                                                      'following': following,
                                                      'post_data': post_data,
                                                      'following_u': following_u,
                                                      'followers_u': followers_u})

    return render(request, 'myapp/userprofile.html', {'user_prf': user_prf,
                                                      'user': user,
                                                      'followers': followers,
                                                      'following': following,
                                                      'post_data': post_data,
                                                      'following_u': following_u,
                                                      'followers_u': followers_u})



@login_required(login_url="/myapp/login/", redirect_field_name='')
def postdetail_viw(request, id):
    user = get_object_or_404(User_info, id=request.user.id)
    user_3 = User_info.objects.filter(id=request.user.id)
    followers = str(user.related_to.all())
    postdet = get_object_or_404(Post_info, id=id)
    comments = Comments.objects.all()
    c = postdet.comments_set.count()
    following = user.user_relationship.filter(to_user__rel_status=1)
    user_1 = User_info.objects.get(id=request.user.id)
    user_2 = postdet.post_user
    form = AddCommentsForm()
    likes = Like.objects.all().distinct()
    like_user = postdet.like_set.filter(like_user=request.user)
    like_usr = user.like_set.all()
    likes_count = postdet.like_set.count()
    if request.method == 'POST':
        if 'del_pst' in request.POST:
            Comments.objects.filter(comm_post=postdet).delete()
            get_object_or_404(Post_info, id=id).delete()
            return HttpResponseRedirect('/myapp/myprofile/')
        if 'add_rel' in request.POST:
            Relationship.objects.get_or_create(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            )
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                     'postdet': postdet,
                                                     'followers': followers,
                                                     'following': following,
                                                     'user_1': user_1,
                                                     'user_2': user_2,
                                                     'user_3': user_3,
                                                     'comments': comments,
                                                     'likes': likes,
                                                     'likes_count': likes_count,
                                                     'c': c,
                                                     'like_user': like_user
                                                     })
        if 'del_rel' in request.POST:
            Relationship.objects.filter(
                rel_from_user=user_1,
                rel_to_user=user_2,
                rel_status=1
            ).delete()
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                     'postdet': postdet,
                                                     'followers': followers,
                                                     'following': following,
                                                     'user_1': user_1,
                                                     'user_2': user_2,
                                                     'user_3': user_3,
                                                     'comments': comments,
                                                     'likes': likes,
                                                     'likes_count': likes_count,
                                                     'c': c,
                                                     'like_user': like_user
                                                             })
        if 'add_comment' in request.POST:
            form = AddCommentsForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.comm_desc = request.POST.get('comm_desc')
                comment.comm_publish_date = timezone.now()
                comment.comm_publish_time = datetime.datetime.now()
                comment.comm_user = user
                comment.comm_post = postdet
                comment.save()
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user
                                                             })

        if 'add_like' in request.POST:
            Like.objects.get_or_create(
                like_user = user,
                like_post = postdet
            )
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user
                                                             })

        if 'del_like' in request.POST:
            Like.objects.filter(
                like_user = user,
                like_post = postdet
            ).delete()
            return render(request, 'myapp/postdetail.html', {'user': user,
                                                             'postdet': postdet,
                                                             'followers': followers,
                                                             'following': following,
                                                             'user_1': user_1,
                                                             'user_2': user_2,
                                                             'user_3': user_3,
                                                             'comments': comments,
                                                             'likes': likes,
                                                             'likes_count': likes_count,
                                                             'c': c,
                                                             'like_user': like_user
                                                             })



    else:
        return render(request, 'myapp/postdetail.html', {'user': user,
                                                         'postdet': postdet,
                                                         'followers': followers,
                                                         'following': following,
                                                         'user_1': user_1,
                                                         'user_2': user_2,
                                                         'user_3': user_3,
                                                         'comments': comments,
                                                         'form': form,
                                                         'c':c,
                                                         'likes': likes,
                                                         'likes_count': likes_count,
                                                         'like_user': like_user,
                                                         'like_usr': like_usr

                                                         })

    return render(request, 'myapp/postdetail.html', {'user': user,
                                                     'postdet': postdet,
                                                     'followers': followers,
                                                     'following': following,
                                                     'user_1': user_1,
                                                     'user_2': user_2,
                                                     'user_3': user_3,
                                                     'comments': comments,
                                                     'form': form,
                                                     'c': c,
                                                     'likes': likes,
                                                     'likes_count': likes_count,
                                                     'like_usr': like_usr
                                                     })



@login_required(login_url="/myapp/login/", redirect_field_name='')
def addpost_viw(request):
    user = get_object_or_404(User_info, id=request.user.id)
    add_post = Post_info.objects.all()
    if request.method == 'POST':
        form = AddPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_user_id = request.user.id
#            post.post_title = request.POST.get('post_title')
#            post.post_desc = request.POST.get('post_desc')
#            post.post_file = request.FILES.get('post_file')
#            post.post_disp_img = request.FILES.get('post_disp_img')
            post.post_publish_date = timezone.now()
            post.post_publish_time = datetime.datetime.now()
#            post.post_video_url = request.POST.get('post_video_url')
#            form.tags = request.POST.get('tags')
            post.save()
            form.save_m2m()
            return HttpResponseRedirect('/myapp/myprofile/')

        else:
            return HttpResponse('Invalid Details!!')
    else:
        form = AddPostForm()
        return render(request, 'myapp/addpost.html', {'form': form,
                                                      'add_post': add_post,
                                                      'user': user})


@login_required(login_url="/myapp/login/", redirect_field_name='')
def useredit_viw(request):
    user = get_object_or_404(User_info, id=request.user.id)
    userlist = User_info.objects.get(username=request.user.username)
    new_passwd = request.POST.get('password')
    rep_passwd = request.POST.get('rep_password')
    if request.method == 'POST':
        if 'info_sav' in request.POST:
            form = UserInfoForm(data=request.POST, files=request.FILES,instance=request.user)
            if new_passwd == rep_passwd:
                if form.is_valid():
                    user.first_name = request.POST.get('first_name', user.first_name)
                    user.last_name = request.POST.get('last_name', user.last_name)
                    user.email = request.POST.get('email', user.email)
                    user.user_country = request.POST.get('user_country', user.user_country)
                    user.user_city = request.POST.get('user_city', user.user_city)
                    user.user_web_url = request.POST.get('user_web_url', user.user_web_url)
                    user.user_pic = request.FILES.get('user_pic', user.user_pic)
                    user.save()
                    return HttpResponseRedirect('/myapp/useredit/')
                else:
                    return HttpResponse('Invalid details!!')
            else:
                return HttpResponse('Passwords did not match!!!')
        if 'pass_sav' in request.POST:
            form = PasswordChangeForm(data=request.POST, instance=request.user)
            old_pass = request.POST.get('old_password')
            new_pass = request.POST.get('password')
            rep_pass = request.POST.get('rep_password')
            if form.is_valid():
                if user.check_password(old_pass):
                    if new_pass == rep_pass:
                        userlist.set_password(form.cleaned_data['password'])
                        userlist.save()
                        return HttpResponseRedirect('/myapp/useredit')
                    else:
                        return HttpResponse('Passwords does not match!!')
                else:
                    return HttpResponse('Invalid password!!')
            else:
                return HttpResponse('Invalid details!!')
        if 'abtme_sav' in request.POST:
            form = AboutMeInfoForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                user.user_abtme_title = request.POST.get('user_abtme_title')
                user.user_abtme_desc = request.POST.get('user_abtme_desc')
                user.save()
                return HttpResponseRedirect('/myapp/useredit')
            else:
                return HttpResponse('Invalid details!!')
    else:
        form = UserInfoForm()
        return render(request, 'myapp/useredit.html', {'user': user,
                                                       'form': form})


def user_authn(request):
    userlist = User_info.objects.all()
    login_form = LoginForm()
    reg_form = RegisterForm()

    if request.method == 'POST':
        if 'signin' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    user_ad = get_object_or_404(User_info, id=request.user.id)
                    return render(request, 'myapp/index.html/', {'user': user,
                                                                 'user_ad': user_ad})
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details!!')
        elif 'signup' in request.POST:
            if request.method == 'POST':
                form = RegisterForm(request.POST, request.FILES)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    Relationship.objects.get_or_create(
                        rel_from_user=user,
                        rel_to_user=user,
                        rel_status=3
                    )
                    return HttpResponseRedirect('/myapp/')
                else:
                    return HttpResponse('Invalid details.')
    else:
        return render(request, "myapp/login.html", {'form': login_form,
                                                    'form': reg_form,
                                                    'userlist': userlist})


@login_required(login_url="/myapp/login/", redirect_field_name='')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/myapp/login/')



def forgot_password(request):
    if request.method == 'POST':
        usernm = request.POST.get('username')
        userfname = request.POST.get('firstname')
        userlname = request.POST.get('lastname')
        usereml = request.POST.get('email')
        usersecques = request.POST.get('secques')
        usersecans = request.POST.get('secans')
        old_pass = request.POST.get('reppass')
        new_pass = request.POST.get('password')
        userlist = User_info.objects.get(username=usernm)
        userfirstname = User_info.objects.get(first_name=userfname)
        userlastname = User_info.objects.get(last_name=userlname)
        useremail = User_info.objects.get(email=usereml)
        userques = User_info.objects.get(user_sec_ques=usersecques)
        userans = User_info.objects.get(user_sec_ans=usersecans)
        form = ForgotPassword(data=request.POST)
        if userlist != 0:
            if userfirstname != 0:
                if userlastname !=0:
                    if useremail !=0:
                        if userques !=0:
                            if userans !=0:
                                if old_pass == new_pass:
                                    if form.is_valid():
                                        userlist.set_password(form.cleaned_data['password'])
                                        userlist.save()
                                        return HttpResponseRedirect('/myapp/login/')
                                    else:
                                        return render(request, 'myapp/login.html', {})
                                else:
                                    HttpResponse('Passwords do not match')
                            else:
                                HttpResponse('Invalid details')
                        else:
                            HttpResponse('Invalid details')
                    else:
                        HttpResponse('Invalid details')
                else:
                    HttpResponse('Invalid details')
            else:
                HttpResponse('Invalid details')
        else:
            HttpResponse('Invalid details')
    else:
        form = ForgotPassword()
        return render(request, "myapp/forgot-password.html", {'form': form})












