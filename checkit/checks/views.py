from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import json

from checkit.activities.models import Activity, Notification
from checkit.checks.models import Check
from checkit.checks.models import Check
from checkit.decorators import ajax_required


FEEDS_NUM_PAGES = 10

@login_required
def feeds(request):
    all_checks = Check.objects.all()
    
    paginator = Paginator(all_checks, FEEDS_NUM_PAGES)
    checks = paginator.page(1)
    
    
    from_check = -1
    
    
    if checks:
        from_check = checks[0].id
        
    
        
        
    return render(request, 'checks/checks.html', {
        'checks': checks,
       
        'from_check': from_check,
        'page': 1,
        })

def feed(request, pk):
    check = get_object_or_404(Check, pk=pk)
    return render(request, 'checks/check.html', {'check': check})

@login_required
@ajax_required
def load(request):
    
    from_check = request.GET.get('from_check')
    page = request.GET.get('page')
    check_source = request.GET.get('check_source')
    all_checks = Check.get_checks(from_check)
    if check_source != 'all':
        all_checks = all_checks.filter(user__id=check_source)
    paginator = Paginator(all_checks, FEEDS_NUM_PAGES)
    try:
        checks = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        checks = []
    html = u''
    csrf_token = unicode(csrf(request)['csrf_token'])
    for check in checks:
        html = u'{0}{1}'.format(html, render_to_string('checks/partial_check.html', {
            'check': check,
            'user': request.user,
            'csrf_token': csrf_token
            })
        )
    return HttpResponse(html)

def _html_checks(last_check, user, csrf_token, check_source='all'):
    checks = Check.get_checks_after(last_check)
    if check_source != 'all':
        checks = checks.filter(user__id=check_source)
    html = u''
    for check in checks:
        html = u'{0}{1}'.format(html, render_to_string('checks/partial_check.html', {
            'check': check,
            'user': user,
            'csrf_token': csrf_token
            })
        )
    return html

@login_required
@ajax_required
def load_new(request):
    last_check = request.GET.get('last_check')
    user = request.user
    csrf_token = unicode(csrf(request)['csrf_token'])
    html = _html_checks(last_check, user, csrf_token)
    return HttpResponse(html)

@login_required
@ajax_required
def check(request):
    last_check = request.GET.get('last_check')
    check_source = request.GET.get('check_source')
    checks = Check.get_checks_after(last_check)
    if check_source != 'all':
        checks = checks.filter(user__id=check_source)
    count = checks.count()
    return HttpResponse(count)

@login_required
@ajax_required
def post(request):
    last_check = request.POST.get('last_feed')
    csrf_token = unicode(csrf(request)['csrf_token'])
    user =request.user 
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0:
        post = post[:255]
        m = Check(user=request.user, post="titan")
        m.save()
    #html = _html_checks(last_check, user, csrf_token)
    html="aaa"
    return HttpResponse(html)

@login_required
@ajax_required
def like(request):
    check_id = request.POST['feed']
    check = Check.objects.get(pk=check_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, check=check_id, user=user)
    if like:
        user.profile.unotify_liked(check)
        like.delete()
    else:
        like = Activity(activity_type=Activity.LIKE, check=check_id, user=user)
        like.save()
        user.profile.notify_liked(check)
    return HttpResponse(check.calculate_likes())

@login_required
@ajax_required
def comment(request):
    if request.method == 'POST':
        check_id = request.POST['feed']
        check = Check.objects.get(pk=check_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:255]
            user = request.user
            check.comment(user=user, post=post)
            user.profile.notify_commented(check)
            user.profile.notify_also_commented(check)
        return render(request, 'checks/partial_check_comments.html', {'check': check})
    else:
        check_id = request.GET.get('feed')
        check = Check.objects.get(pk=check_id)
        return render(request, 'checks/partial_check_comments.html', {'check': check})

@login_required
@ajax_required
def update(request):
    first_check = request.GET.get('first_feed')
    last_check = request.GET.get('last_feed')
    check_source = request.GET.get('feed_source')
    checks = Check.get_checks().filter(id__range=(last_check, first_check))
    if check_source != 'all':
        checks = checks.filter(user__id=check_source)
    dump = {}
    for check in checks:
        dump[check.pk] = {'likes': check.likes, 'comments': check.comments}
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')

@login_required
@ajax_required
def track_comments(request):
    check_id = request.GET.get('feed')
    check = Check.objects.get(pk=check_id)
    return render(request, 'checks/partial_check_comments.html', {'check': check})

@login_required
@ajax_required
def remove(request):
    try:
        check_id = request.POST.get('feed')
        check = Check.objects.get(pk=check_id)
        if check.user == request.user:
            likes = check.get_likes()
            parent = check.parent
            for like in likes:
                like.delete()
            check.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception, e:
        return HttpResponseBadRequest()
