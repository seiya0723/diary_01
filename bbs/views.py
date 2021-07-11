from django.shortcuts import render,redirect
from django.views import View


from .models import Topic
from .forms import TopicForm

import datetime 


class BbsView(View):

    def get(self, request, *args, **kwargs):

        if "month" in request.GET and "year" in request.GET:
            print(request.GET["month"])
            print(request.GET["year"])

            topics  = Topic.objects.filter(dt__year=request.GET["year"],dt__month=request.GET["month"])
            dt  = datetime.date(int(request.GET["year"]),int(request.GET["month"]),1)
        else:
            topics  = Topic.objects.all()

            dt  = datetime.datetime.now()
            dt  = dt.replace(day=1)

        year        = dt.year
        month       = dt.month
        days        = []
        weekdays    = []

        #.weekday()で数値化した曜日が出力される(月曜日が0、日曜日が6)
        #一ヶ月の最初が日曜日であればそのまま追加、それ以外の曜日であれば、曜日の数値に1追加した数だけ空文字を追加
        if dt.weekday() != 6:
            for i in range(dt.weekday()+1):
                weekdays.append("")

        #1日ずつ追加して月が変わったらループ終了
        while month == dt.month:
            weekdays.append(str(dt.day))
            dt  = dt + datetime.timedelta(days=1)
            if dt.weekday() == 6:
                days.append(weekdays)
                weekdays    = []

        if dt.weekday() != 6:
            days.append(weekdays)
            weekdays    = []

        print(days)

        """
        [ ['  ', '  ', '1 ', '2 ', '3 ', '4 ', '5 '],
          ['6 ', '7 ', '8 ', '9 ', '10', '11', '12'],
          ['13', '14', '15', '16', '17', '18', '19'],
          ['20', '21', '22', '23', '24', '25', '26'],
          ['27', '28', '29', '30']
          ]
        """



        context = { "topics":topics,
                    "days":days,
                    "year":year,
                    "month":month,
                }


        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):


        form    = TopicForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("bbs:index")



index   = BbsView.as_view()

