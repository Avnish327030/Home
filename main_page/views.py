from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render,redirect
from main_page.models import Member
from main_page.forms import MemberForm
from main_page.models import Member_expense
from main_page.forms import Member_exp
from Manager.models import Manager
# Create your views here.
def display(request):
    if 'manager_id' in request.session:

        id=request.session['manager_id']
        if request.method=='POST':
            name=str(request.POST['mname'])
            member=Member.objects.filter(fname__contains=name,manager_id__exact=request.session['manager_id'])
            if member.count() == 0:
                messages.error(request, "Sorry !! No match found ...")
            context = {'name': id, 'm': member}
            return render(request, 'memberdetail.html', context)
        member=Member.objects.filter(manager_id__exact=request.session['manager_id'])
        if member.count()==0:
            messages.error(request,"You do not have member. please!! add member to your account ")
        context={'name':id,'m':member}
        return render(request, 'memberdetail.html', context)
    else:
        messages.error(request,"Please !! login to your account ")
        return redirect('login')

def manage_member(request):
    if 'manager_id' in request.session:
        id = request.session['manager_id']
        manager = Manager.objects.get(manager_id=id)
        if request.method=='POST':
            member_form=MemberForm(request.POST or None,request.FILES or None)
            if member_form.is_valid():
                member_form.save()
                messages.success(request,"Member added successfully")
                return redirect('managemember')
            else:
                messages.error(request,"Error occured!! while adding to Member ")
                member = Member.objects.filter(manager_id__exact=request.session['manager_id'])
                context={'member_form':MemberForm(request.POST),'m':member}
                return render(request,'managemember.html',context)
        member = Member.objects.filter(manager_id__exact=request.session['manager_id'])
        member_form=MemberForm(initial={'manager_id':id})
        context={'name':id,'member_form':member_form,'m':member}
        return render(request, 'managemember.html', context)
    else:
        messages.error(request, "Please !! login to your account ")
        return redirect('login')


def delete(request):
    if request.method=='POST':
        mid=int(request.POST['member_id'])
        Member.objects.filter(member_id__exact=mid).delete()
        member = Member.objects.filter(manager_id__exact=request.session['manager_id'])
        context = {'member_form': MemberForm(), 'm': member}
        messages.success(request,'Member remove successfully')
        return redirect('managemember')

def expendituredetail(request):
    if 'manager_id' in request.session:
        id = request.session['manager_id']
        mid = Member.objects.filter(manager_id__exact=id).order_by('member_id')
        no_of_mem = mid.count()
        amount = {}
        for m in mid:
            amount[m.member_id] = Member_expense.objects.filter(member_id=m.member_id).values('amount').aggregate(Sum('amount'))
        context = {'amount': amount,'Manager_id':id,'no_of_mem':no_of_mem,'mid':mid}
        return render(request, 'expendituredetail.html', context)
    else:
        messages.error(request, "Please !! login to your account ")
        return redirect('login')

def update_exp(request):
    if 'manager_id' in request.session:
        id = request.session['manager_id']
        manager = Manager.objects.get(manager_id=id)
        if request.method=='POST':
            memb_id=request.POST['member_id']
            date=request.POST['date_exp']
            x=Member_expense()
            x.manager_id=manager
            x.member_id=Member.objects.get(member_id=memb_id)
            x.date_exp=request.POST['date_exp']
            x.amount=request.POST['amount']
            x.save()
            messages.success(request,"Updated successfully")
            return redirect('expendituredetail')
        exp = Member_exp(manager)

        members=Member.objects.filter(manager_id__exact=id)
        context = {'update_exp': exp,'m':members,'c':members}

        return render(request, 'updateexp.html', context)
    else:
        messages.error(request, "Please !! login to your account ")
        return redirect('login')


def exp_getdetail(request):
    member_id=int(request.POST['member_id'])
    manager_id=str(request.POST['manager_id'])
    mem_name=Member.objects.get(member_id=member_id)
    member_det=Member_expense.objects.filter(manager_id=manager_id).filter(member_id=member_id).order_by('date_exp')
    amount=member_det.aggregate(Sum('amount'))
    context={'member_detail':member_det,'c':member_det.count(),'Manager_name':request.session['manager_name'],'Member_name':mem_name.fname,'amount':amount,'member_id':member_id,'manager_id':manager_id}
    return render(request,'member_getdetail.html',context)

def exp_getdetailbydate(request):
    if request.method=='POST':
        fdate = request.POST['from_date']
        tdate = request.POST['to_date']
        member_id = int(request.POST['member_id'])
        manager_id = str(request.POST['manager_id'])
        mem_name = Member.objects.get(member_id=member_id)
        member_det = Member_expense.objects.filter(manager_id=manager_id).filter(member_id=member_id).filter(date_exp__range=[fdate,tdate])
        amount = member_det.aggregate(Sum('amount'))
        context = {'member_detail': member_det, 'c': member_det.count(),
                   'Manager_name': request.session['manager_name'], 'Member_name': mem_name.fname, 'amount': amount,
                   'member_id': member_id,'manager_id':manager_id}
        return render(request, 'member_getdetail.html', context)

def expenditurereport(request):
    if 'manager_id' in request.session:
        id = request.session['manager_id']
        if request.method=='POST':
            mid = Member.objects.filter(manager_id__exact=id).order_by('member_id')
            no_mem=int(request.POST['no_of_mem'])
            tot_am=int(request.POST['tot_am'])
            charge=tot_am/no_mem
            x={}
            amount={}
            for i in range(1,no_mem+1):
                x[i]=int(request.POST['mem'+str(i)])
                amount[x[i]]=int(request.POST[str(x[i])])
            res={}
            for a,b in amount.items():
                if charge<b:
                    am=b-charge
                    res[a]={'message':"You have to get ",'amount':round(am),'spend':b}
                elif charge>b:
                    am=charge-b
                    res[a]={'message':"You have to return",'amount':round(am),'spend':b}
                else:
                    am=0
                    res[a]={'message':"Good news!! not need any transaction",'amount':am,'spend':b}

            context={'no_mem':no_mem,'charge':round(charge),'res':res,'mid':mid}
            return render(request,'final.html',context)
        else:
            mid = Member.objects.filter(manager_id__exact=id).order_by('member_id')
            no_of_mem=mid.count()
            amount={}
            for m in mid:
                amount[m.member_id]= Member_expense.objects.filter(member_id=m.member_id).values( 'amount').aggregate(Sum('amount'))

            Total_amount=Member_expense.objects.filter(member_id__in=mid).values('amount','member_id').aggregate(Sum('amount'))
            context = {'exp': mid,'no_of_mem':no_of_mem ,'mid':mid,'amount':amount,'total_amount':Total_amount,'manager_id':id}
            return render(request,'expenditurereport.html',context)
    else:
        messages.error(request, "Please !! login to your account ")
        return redirect('login')
def expenditurereportbydate(request):
    if request.method == 'POST':
        fdate = request.POST['from_date']
        tdate = request.POST['to_date']
        manager_id = str(request.POST['manager_id'])
        mid = Member.objects.filter(manager_id__exact=manager_id).order_by('member_id')
        no_of_mem = mid.count()
        amount = {}
        for m in mid:
            amount[m.member_id] = Member_expense.objects.filter(member_id=m.member_id).filter(date_exp__range=[fdate, tdate]).values('amount').aggregate(Sum('amount'))

        Total_amount = Member_expense.objects.filter(member_id__in=mid).filter(date_exp__range=[fdate, tdate]).values('amount', 'member_id').aggregate(
            Sum('amount'))
        context = {'exp': mid, 'no_of_mem': no_of_mem, 'mid': mid, 'amount': amount, 'total_amount': Total_amount,
                   'manager_id': id}
        return render(request, 'expenditurereport.html', context)

def deletedetail(request):
    if 'manager_id' in request.session:
        if request.method == 'POST':
            fdate=request.POST['from_date']
            tdate=request.POST['to_date']
            manager_id=str(request.session['manager_id'])
            Member_expense.objects.filter(manager_id__exact=manager_id,date_exp__range=[fdate, tdate]).delete()
            messages.success(request,"Expense detail deleted successfully")
            return render(request,'deletedetail.html',{'help':"Delete your expense record select date to do it."})
        return render(request,'deletedetail.html',{'help':"Delete your expense record select date to do it."})
    else:
        messages.error(request, "Please !! login to your account ")
        return redirect('login')
