

from django.contrib.auth import authenticate

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.template import context

from appLicenta.forms import PfpForm, ImageForm
from appLicenta.models import User, Test, Project, Bug, TestStatus, BugStatus, Testcontent, User2Test, User2Project, \
    User2Bug, Bugcontent


def home(request, pk, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.logged_in:
        project = get_object_or_404(Project, pk=pk)
        tests = Test.objects.filter(project_id=pk)
        bugs = Bug.objects.filter(project_id=pk)


        user2project = User2Project.objects.filter(user_id=user.pk, project_field=project.pk).first()

        if request.method == 'GET':
            if request.GET.get('search') is not "" and request.GET.get('search') is not None:
                projects = Project.objects.filter(title__icontains=request.GET.get('search'))
                return render(request, 'home.html',{'project': project, 'pk': pk, 'projects': projects,
                                                'range': range(15-projects.count()), 'tests': tests, 'bugs': bugs, 'user': user, 'user2project':user2project})

        if request.method == 'POST':
            if request.POST['save'] == 'newTest':
                title = request.POST.get('t_title')
                preq = request.POST.get('t_preq')

                prio = request.POST.get('t_prio')
                desc = request.POST.get('t_desc')
                steps = request.POST.get('t_steps')
                results = request.POST.get('t_results')
                pr_id = project.pk
                new_test = Test(title=title, prerequisites=preq, priority=prio ,description=desc,steps=steps, results=results, project_id=pr_id)
                new_test.save()

                new_test_status = TestStatus(defined_1=True, defined_2=True, defined_3=True, defined_4=True, test_id=new_test.pk)
                new_test_status.save()
            if request.POST['save'] == 'newBug':
                title = request.POST.get('b_title')
                prio = request.POST.get('b_prio')
                desc = request.POST.get('b_desc')
                steps = request.POST.get('b_steps')
                impact = request.POST.get('b_impact')
                pr_id = project.pk
                new_bug = Bug(title=title, priority=prio, description=desc, steps=steps, impact=impact, project_id=pr_id)
                new_bug.save()

                new_bug_status = BugStatus(detected_1=True, detected_2=True, detected_3=True,bug_id=new_bug.pk)
                new_bug_status.save()

            if request.POST['save'] == 'newPrj':
                title = request.POST.get('p_title')
                desc = request.POST.get('p_desc')

                new_prj = Project(title=title, description=desc)
                new_prj.save()
                return redirect('home', new_prj.pk, user.pk)
            if request.POST['save'] == 'assignProject':
                user2project = User2Project(user_id=user.pk, project_field_id=project.pk)
                user2project.save()
                return redirect('home', project.pk, user.pk)
            if request.POST['save'] == 'abandonProject':
                user2project = User2Project.objects.get(user_id=user.pk, project_field_id=project.pk)
                user2project.delete()
                return redirect('home', project.pk, user.pk)

            if request.POST['save'] == 'editPrj':
                title = request.POST.get('p_title')
                desc = request.POST.get('p_desc')
                project.title = title
                project.description = desc
                project.save()
                return redirect('home', project.pk, user.pk)

            if request.POST['save'] == 'logout':
                user.logged_in = False
                user.save()
                return redirect('login')

        projects = Project.objects.all()
        return render(request,'home.html',{'project': project, 'projects': projects[:30],
                                           'range': range(15-projects.count()), 'tests': tests, 'bugs': bugs, 'user': user, 'user2project': user2project})
    else:
        return redirect('login')

def about(request):
    return render(request, 'about.html')


def login(request):
    if request.method == 'POST':
        if request.POST['save'] == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.get(email = email)
            projects = Project.objects.all()
            proiect = projects.first()
            if user is not None and user.password == password:
                user.logged_in = True
                user.save()
                return redirect('home', proiect.pk, user.pk)

            else:
                return render(request, 'login.html')
        if request.POST['save'] == 'register':
            return redirect('register')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        if request.POST['save'] == 'register':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confpassword = request.POST.get('confpassword')

            if password != confpassword:
                HttpResponse("Passwords don't match")
                return render(request,'register.html')
            print(username)
            print(password)
            print(email)
            user = User(username=username, email=email, password=password)
            user.save()

            return redirect('login')
        if request.POST['save'] == 'login':
            return redirect('login')
    return render(request, 'register.html')


def profile(request, user_id, connected_user_id):
    user = get_object_or_404(User, pk=user_id)
    connected_user = get_object_or_404(User, pk=connected_user_id)
    if connected_user.logged_in:

        projects = Project.objects.all()
        project = projects.first()

        test_id_list = []
        prj_id_list = []
        bug_id_list = []
        userTestList = None
        userBugList = None
        userProjectList = None
        user2testlist = User2Test.objects.filter(user=user)
        print(user.id)
        print(user2testlist)
        user2test = user2testlist.first()

        for test in user2testlist:
            test_id_list.append(test.test_id)

        print(test_id_list)
        user2buglist = User2Bug.objects.filter(user_id=user.id)
        user2bug = user2buglist.first()

        for bug in user2buglist:
            bug_id_list.append(bug.bug_id)

        user2projectlist = User2Project.objects.filter(user_id=user.id)
        user2project = user2projectlist.first()

        for prj in user2projectlist:
            prj_id_list.append(prj.project_field_id)

        if user2test is not None:
            userTestList = Test.objects.filter(id__in=test_id_list)
            print(userTestList.values())

        if user2bug is not None:
            userBugList = Bug.objects.filter(id__in=bug_id_list)
            print(userBugList.values())

        if user2project is not None:
            userProjectList = Project.objects.filter(id__in=prj_id_list)
            print(userProjectList.values())

        if request.method == 'GET':
            if request.GET.get('search') is not "" and request.GET.get('search') is not None:
                projects = Project.objects.filter(title__icontains=request.GET.get('search'))
                return render(request, 'profile.html', {'project': project, 'projects': projects
                                                        , 'range': range(15 - projects.count()), 'user': user, 'connected_user': connected_user
                                                        , 'userTestList': userTestList, 'userBugList':userBugList, 'userProjectList':userProjectList, 'imgform': PfpForm()})

        if request.method == 'POST':
            if request.POST['save'] == 'editProfile':
                user.username = request.POST.get('u_username')
                print(user.username)

            if request.POST['save'] == 'changePfp':
                form = PfpForm(request.POST, request.FILES)
                if form.is_valid():
                    image = form.cleaned_data['image']
                    user.image = image
                    user.save()
                    return redirect('profile', user.id, connected_user.id)

            if request.POST['save'] == 'changePass':
                oldpass = request.POST.get('oldpass')

                newpass = request.POST.get('newpass')

                repeatpass = request.POST.get('repeatpass')

                if user.password == oldpass and newpass == repeatpass:
                    user.password = newpass
                    user.save()
                else:
                    return redirect('profile', user.id, connected_user.id)

            if request.POST['save'] == 'logout':
                connected_user.logged_in = False
                connected_user.save()
                return redirect('login')

        return render(request, 'profile.html', {'project': project,'projects':projects, 'range': range(15 - projects.count())
            ,'user': user, 'connected_user': connected_user, 'userTestList': userTestList, 'userBugList':userBugList, 'userProjectList':userProjectList, 'imgform': PfpForm()})
    else:
        return redirect('login')


def test(request, pk, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.logged_in:
        test = Test.objects.get(id=pk)
        description = test.description
        test_status = TestStatus.objects.get(test_id=test.pk)
        project = Project.objects.get(id=test.project.id)


        user2test = User2Test.objects.filter(user_id=user.pk, test_id=test.pk).first()

        responsibleUsers = User2Test.objects.filter(test_id=test.pk)
        content = Testcontent.objects.filter(test_id= test.id)
        print(responsibleUsers)
        if request.method == 'GET':
            if request.GET.get('search') is not "" and request.GET.get('search') is not None:
                projects = Project.objects.filter(title__icontains=request.GET.get('search'))
                return render(request, 'test.html', {'project': project, 'projects': projects, 'test': test,
                                                     'description': description, 'range': range(15 - projects.count()),
                                                     'test_status': test_status ,'user': user, 'user2test': user2test, 'responsibleUsers':responsibleUsers, 'imgform': ImageForm(), 'content': content})
        if request.method == 'POST':
            if request.POST['test'] == 'editTest':
                test.prerequisites = request.POST.get('t_preq')

                test.priority = request.POST.get('t_prio')
                test.description = request.POST.get('t_desc')
                test.steps = request.POST.get('t_steps')
                test.results = request.POST.get('t_results')
                test.save()

                if request.POST.get('t_content'):
                    # test_file = request.POST.get('t_content')
                    # print(test_file)
                    test_content = request.FILES['t_content']
                    print(test_content)
                    print(test_content.value())
                    testcontent = Testcontent( test_id=test.pk)
                    testcontent.save()

                return redirect('test', test.pk, user.pk)
            if request.POST['test'] == 'statusTest':
                test_status.specified_1 = not(request.POST.get('specified11') is None)
                test_status.specified_2 = not(request.POST.get('specified12') is None)
                test_status.specified_3 = not(request.POST.get('specified13') is None)
                test_status.specified_4 = not(request.POST.get('specified14') is None)
                test_status.specified_5 = not(request.POST.get('specified15') is None)
                test_status.specified_6 = not(request.POST.get('specified16') is None)

                spec = test_status.specified_1 == True and test_status.specified_2 == True and test_status.specified_3 == True and test_status.specified_4 == True and test_status.specified_5 == True and test_status.specified_6 == True

                if spec:
                    test_status.executed_1 = not(request.POST.get('executed11') is None)
                    test_status.executed_2 = not(request.POST.get('executed12') is None)
                    exec = test_status.executed_1 == True and test_status.executed_2 == True
                    if exec:
                        test_status.evaluated_1 = not(request.POST.get('evaluated11') is None)
                        test_status.evaluated_2 = not(request.POST.get('evaluated12') is None)
                        test_status.evaluated_3 = not(request.POST.get('evaluated13') is None)
                        eval = test_status.evaluated_1 == True and test_status.evaluated_2 == True and test_status.evaluated_3 == True
                    else:
                        exec = False
                        test_status.evaluated_1 = False
                        test_status.evaluated_2 = False
                        test_status.evaluated_3 = False
                        eval = False
                else:
                    spec = False
                    test_status.executed_1 = False
                    test_status.executed_2 = False
                    exec = False
                    test_status.evaluated_1 = False
                    test_status.evaluated_2 = False
                    test_status.evaluated_3 = False
                    eval = False

                if request.POST.get('t_outc') is not None and spec and exec and eval:
                    test.outcome = request.POST.get('t_outc')
                    test.save()
                else:
                    test.outcome = '-'
                    test.save()
                test_status.save()
                return redirect('test', test.pk, user.pk)
            if request.POST['test'] == 'assignTest':
                user2test = User2Test(user_id = user.pk, test_id = test.pk)
                user2test.save()

                return redirect('test', test.pk, user.pk)

            if request.POST['test'] == 'logout':
                user.logged_in = False
                user.save()
                return redirect('login')

            if request.POST['test'] == 'abandonTest':
                user2test = User2Test.objects.get(user_id = user.pk, test_id = test.pk)
                user2test.delete()

                return redirect('test', test.pk, user.pk)
            if request.POST['test'] == 'addContent':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                    image = form.cleaned_data['image']
                    testContent = Testcontent(content=image, test_id = test.id)
                    testContent.save()
                    return redirect('test', test.id, user.id)

        projects = Project.objects.all()

        return render(request, 'test.html', {'test': test, 'description': description, 'project': project,
                                             'projects': projects[:30], 'range': range(15-projects.count()), 'test_status': test_status,
                                             'user': user, 'user2test': user2test, 'responsibleUsers': responsibleUsers, 'imgform': ImageForm(), 'content': content})
    else:
        return redirect('login')


def bug(request, pk, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.logged_in:
        bug = Bug.objects.get(id=pk)
        project = Project.objects.get(id=bug.project_id)
        user2bug = User2Bug.objects.filter(user_id=user.id, bug_id=bug.id).first()
        bug_status = BugStatus.objects.get(bug_id=bug.id)

        responsibleUsers = User2Bug.objects.filter(bug_id=bug.pk)
        content = Bugcontent.objects.filter(bug_id=bug.id)

        if request.method == 'GET':
            if request.GET.get('search') is not "" and request.GET.get('search') is not None:
                projects = Project.objects.filter(title__icontains=request.GET.get('search'))
                return render(request, 'bug.html', {'project': project, 'projects': projects, 'bug': bug,
                                                     'range': range(15 - projects.count()), 'user': user, 'user2bug': user2bug, 'bug_status': bug_status,
                                                    'responsibleUsers':responsibleUsers,'imgform': ImageForm(), 'content': content})

        if request.method == 'POST':
            if request.POST['save'] == 'logout':
                user.logged_in = False
                user.save()
                return redirect('login')

            if request.POST['save'] == 'assignBug':
                user2bug = User2Bug(user_id = user.pk, bug_id = bug.pk)
                user2bug.save()

                return redirect('bug', bug.pk, user.pk)

            if request.POST['save'] == 'editBug':
                bug.priority = request.POST.get('b_prio')
                bug.impact = request.POST.get('b_imp')
                bug.description = request.POST.get('b_desc')
                bug.location =request.POST.get('b_loc')
                bug.steps = request.POST.get('b_steps')
                bug.save()

                return redirect('bug', bug.pk, user.pk)
            if request.POST['save'] == 'statusBug':
                bug_status.located_1 = not(request.POST.get('located11') is None)
                bug_status.located_2 = not(request.POST.get('located12') is None)
                bug_status.located_3 = not(request.POST.get('located13') is None)
                bug_status.located_4 = not(request.POST.get('located14') is None)

                located = bug_status.located_1 == True and bug_status.located_2 == True and bug_status.located_3 == True and bug_status.located_4 == True

                if located:
                    bug_status.fixed_1 = not(request.POST.get('fixed11') is None)
                    bug_status.fixed_2 = not(request.POST.get('fixed12') is None)
                    bug_status.fixed_3 = not (request.POST.get('fixed13') is None)
                    fixed = bug_status.fixed_1 == True and bug_status.fixed_2 == True and bug_status.fixed_3 == True
                    if fixed:
                        bug_status.closed_1 = not(request.POST.get('closed11') is None)
                        bug_status.closed_2 = not(request.POST.get('closed12') is None)
                        closed = bug_status.closed_1 == True and bug_status.closed_2 == True
                    else:
                        fixed = False
                        bug_status.closed_1 = False
                        bug_status.closed_2 = False
                        closed = False
                else:
                    located = False
                    bug_status.fixed_1 = False
                    bug_status.fixed_2 = False
                    bug_status.fixed_3 = False
                    fixed = False
                    bug_status.closed_1 = False
                    bug_status.closed_2 = False
                    closed = False
                bug_status.save()
                return redirect('bug', bug.pk, user.pk)

            if request.POST['save'] == 'abandonBug':
                user2bug = User2Bug.objects.get(user_id = user.pk, bug_id = bug.pk)
                user2bug.delete()

                return redirect('bug', bug.pk, user.pk)

            if request.POST['save'] == 'addContent':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                    image = form.cleaned_data['image']
                    bugContent = Bugcontent(content=image, bug_id=bug.id)
                    bugContent.save()
                    return redirect('bug', bug.id, user.id)

        projects = Project.objects.all()

        return render(request, 'bug.html', {'project': project, 'projects': projects, 'bug': bug,
                                            'range': range(15 - projects.count()), 'user': user, 'user2bug': user2bug, 'bug_status': bug_status,
                                            'responsibleUsers': responsibleUsers, 'imgform': ImageForm(), 'content': content})
    else:
        return redirect('login')


def practice(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.logged_in:
        projects = Project.objects.all()
        project = projects.first()

        if request.method == 'GET':
            if request.GET.get('search') is not "" and request.GET.get('search') is not None:
                projects = Project.objects.filter(title__icontains=request.GET.get('search'))
                return render(request, 'practice.html', {'project': project, 'projects': projects
                                                        , 'range': range(15 - projects.count()), 'user': user})

        if request.method == 'POST':
            if request.POST['save'] == 'logout':
                user.logged_in = False
                user.save()
                return redirect('login')

        return render(request, 'practice.html', {'user':user, 'project': project, 'projects': projects
                                                        , 'range': range(15 - projects.count())})
    else:
        return redirect('login')


def activityflow(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.logged_in:
        projects = Project.objects.all()
        project = projects.first()

        if request.method == 'GET':
            if request.GET.get('search') is not "" and request.GET.get('search') is not None:
                projects = Project.objects.filter(title__icontains=request.GET.get('search'))
                return render(request, 'activityflow.html', {'project': project, 'projects': projects
                                                        , 'range': range(15 - projects.count()), 'user': user})

        if request.method == 'POST':
            if request.POST['save'] == 'logout':
                user.logged_in = False
                user.save()
                return redirect('login')

        return render(request, 'activityflow.html', {'user': user, 'project': project, 'projects': projects
                                                        , 'range': range(15 - projects.count())})
    else:
        return redirect('login')


def landing(request):
    return redirect('login')