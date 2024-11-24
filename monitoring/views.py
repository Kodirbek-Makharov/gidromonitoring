from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from .models import Noqonuniy_holat_turi, Viloyat, Tuman, Stansiya, Dalolatnoma, DalolatnomaRasm
from .forms import DalolatnomaForm
from .middleware import login_exempt
from django.http import HttpResponse
from pprint import pprint
import datetime 
# from django.contrib.auth.decorators import login_required
# Create your views here.


def has_group(user, group):
    return user.groups.filter(name=group).exists()

@login_exempt
# @login_required
def seed(request):
    holatlar = ['Ер ости сувларига гидрогеологик хулосасиз қудуқ бурғилаш',
	'Ер ости сувларига рухсатномасиз қудуқ бурғилаш',
	'Ер ости сувларига қудуқ бурғилагандан сўнг қудуқ техник паспортини топширмаслик',
    'Ер ости сувларидан рухсатномасиз фойдаланиш',
	'Ер ости сувларидан фойдаланишда йиллик ҳисобот топширмаслик',
	'Ер ости сувларидан счётчиксиз фойдаланиш',
    'Кузатув қудуқларини ишдан чиқариш'
    ]

    stansiyalar = [['Қорақалпоқ станцияси','QRQ'],	['Андижон станцияси', 'AND'],
	['Бухоро станцияси', 'BXR'],	['Жиззах станцияси', 'JZX'],	['Қашқадарё станцияси', 'QSHQ'],
    ['Навоий станцияси', 'NAV'],	['Наманган станцияси', 'NAM'],    ['Самарқанд станцияси', 'SAM'],
    ['Сирдарё станцияси', 'SRD'],	['Сурхондарё станцияси', 'SUR'],	['Тошкент станцияси', 'TSHK'],
    ['Фарғона станцияси', 'FAR'],	['Хоразм станцияси', 'XOR']]

    for h in holatlar:
        Noqonuniy_holat_turi.objects.create(nomi=h)
    for s in stansiyalar:
        Stansiya.objects.create(nomi=s[0], seriya=s[1])


    viloyatlar = {'Қорақалпоғистон Республикаси':['Нукус шаҳри','Амударё','Беруний','Бозатов','Қанликўл','Қораўзак','Кегейли','Қўнғирот','Мўйноқ','Нукус','Тахиатош','Тахтакўпир','Тўрткўл ','Хўжайли','Чимбой','Шуманой','Элликқальа'],
    'Андижон вилояти':['Андижон шаҳри','Андижон шаҳри','Асака','Балиқчи','Бўстон','Булоқбоши','Избоскан','Жалақудуқ','Хўжаобод','Қўрғонтепа','Марҳамат','Олтинкўл','Пахтаобод','Шаҳрихон','Улуғнор','Хонабод шаҳри'],
    'Бухоро вилояти':['Бухоро шаҳри','Олот','Ғиждувон','Жондор','Когон','Қоракўл','Қоровулбозор','Пешку','Ромитан','Шофиркон','Вобкент','Когон шаҳри','Галаосиё шаҳри','Вобкент шаҳри','Газли шаҳри','Олот шаҳри','Ромитан шаҳри','Шофиркон шаҳри','Қоракўл шаҳри','Қоровулбозор шаҳри','Ғиждувон шаҳри'],
	'Жиззах вилояти':['Жиззах шаҳри','Арнасой','Бахмал','Дўстлик','Фориш','Ғаллаорол','Шароф Рашидов','Мирзачўл','Пахтакор','Янгиобод','Зомин','Зафаробод','Зарбдор'],
    'Қашқадарё вилояти':['Қарши шаҳри','Деҳқонобод','Касби','Китоб','Косон','Кўкдала','Миришкор','Муборак','Нишон','Қамаши','Қарши ','Яккабоғ','Ғузор','Шаҳрисабз','Чироқчи','Бушкент шаҳри','Китоб шаҳри','Косон шаҳри','Муборак шаҳри','Талимаржон шаҳри','Чироқчи шаҳри','Шаҳрисабз шаҳри','Яккабоғ шаҳри','Янги Нишон шаҳри','Қамаши шаҳри','Ғузор шаҳри'],
    'Навоий вилояти':['Навоий шаҳри','Конимех','Кармани','Қизилтепа','Хатирчи','Навбаҳор','Нурота','Томди','Учқудуқ','Зарафшон шаҳри'],
    'Наманган вилояти':['Наманган шаҳри','Чортоқ','Чуст','Косонсой','Мингбулоқ','Наманган','Норин','Поп','Тўрақўрғон','Учқўрғон','Уйчи','Янгиқўрғон','Давлатобод','Янги Наманган','Наманган шаҳри','Косонсой шаҳри','Поп шаҳри','Тўрақўрғон шаҳри','Учқўрғон шаҳри','Чортоқ шаҳри','Чуст шаҳри','Ҳаққулобод шаҳри'],
    'Самарқанд вилояти':['Самарқанд шаҳри','Булунғур','Иштихон','Жомбой','Каттақўрғон','Қўшработ','Нарпай','Нуробод','Оқдарё','Пахтачи','Пайариқ','Пастдарғом','Самарқанд','Тойлоқ','Ургут','Каттақўрғон шаҳри'],
    'Сирдарё вилояти':['Гулистон шаҳри','Оқолтин','Бойовут','Гулистон','Ховос','Мирзаобод','Сардоба','Сайхунобод','Сирдарё','Бахт шаҳри','Сирдарё шаҳри','Ширин шаҳри','Янгиер шаҳри'],
    'Сурхондарё вилояти':['Бандихон','Музработ','Қизириқ','Узун','Бойсун','Жарқўрғон','Олтинсой','Қумқўрғон','Шеробод','Шўрчи','Термиз шаҳри','Термиз ','Ангор','Денов','Сариосиё'],
    'Тошкент вилояти':['Бекобод тумани','Бўка тумани','Бўстонлиқ тумани','Чиноз тумани','Ўртачирчиқ тумани','Оҳангарон тумани','Оққўрғон тумани','Паркент тумани','Пискент тумани','Қибрай тумани','Қуйичирчиқ тумани','Янгийўл тумани','Юқоричирчиқ тумани','Зангиота тумани','Ангрен шаҳри','Бекобод шаҳри','Чирчиқ шаҳри','Олмалиқ шаҳри','Оҳангарон  шаҳри','Янгийўл  шаҳри'],
	'Тошкент шаҳри':['Бектемир','Чилонзор','Миробод','Мирзо Улуғбек','Олмазор','Сергели','Шайҳонтоҳур','Учтепа','Яккасарой','Яшнаобод','Янгихаёт','Юнусобод'],
    'Фарғона вилояти':['Бешариқ','Боғдод','Бувайда','Данғара','Фарғона шаҳри','Фарғона','Фурқат','Марғилон шаҳри','Ўзбекистон','Олтиариқ','Қўқон шаҳри','Қўштепа','Қува','Қувасой шаҳри','Риштон','Сўх','Тошлоқ','Учкўприк','Ёзёвон'],
    'Хоразм вилояти':['Боғот','Гурлан','Қўшкўпир','Шовот','Урганч шаҳри','Урганч ','Хазорасп','Хива шаҳри','Хива','Хонқа','Янгиариқ','Янгибозор'],
    }

    for v,tumanlar in viloyatlar.items():
        viloyat = Viloyat.objects.create(nomi=v)
        for t in tumanlar:
            Tuman.objects.create(nomi=t, viloyat=viloyat)

    symbols = (u"абвгдеёжзийклмнопрстуфхҳцчшщъыьэюяўғқАБВГДЕЁЖЗИЙКЛМНОПРСТУФХҲЦЧШЩЪЫЬЭЮЯЎҒҚ",
               u"abvgdeejziyklmnoprstufxhscss_y_euaugqABVGDEEJZIYKLMNOPRSTUFXHSCSS_Y_EUAUGQ")
    tr = {ord(a):ord(b) for a, b in zip(*symbols)}

    from django.contrib.auth.models import Group
    from django.contrib.auth.models import User

    Group.objects.create(name='administrator')
    g,c = Group.objects.get_or_create(name='inspektor')
    inspektorlar = ['Бегматов Расулжон Мамажонович','Бимурзаев Гани Амиргалиевич','Анорбоев Фазлиддин Зайнитдин ўғли','Уралов Ибрагим Фахридинович','Мелиқулов Равшан Алимардонович','Еркебаев Сапаргали Турабекович','Тураббаев Акмалбек Толибаевич','Сааитуллоев Бехрўз Асомидинович','Тўхтамуродов Камолжон Комилжон ўғли','Юсупов Собир Мусаевич','Нишонов Мухторжон Эсоналиевич','Тўғонов Абдумалик Рахимович','Бобоназаров Бектош Абдуллаевич','Душанов Аброр Кенжаевич','Курбанов Тошкан Ҳамдамович','Рўзиқулов Гайрат Бахтиёрович','Кодиров Олимбай Халилович','Қулдошев Баҳром Эшмурод ўғли','Яллакабилов Акбар Ғуломович','Анорбоев Ахрор Акрамович','Омантурдиев Бахриддин Расулович','Базаров Хасан Шерданакулович','Айтметов Бобир Рустемович','Исабаев Кодир Абдуллаевич','Бердиев Хусан Учкунович','Есенбаев Гаибидулла Реимбаевич','Собитов Достонбек Рустам ўғли','Эшанкулов Аманжан Рустамович','Жуманов Эшпулат  Тожиевич','Исматуллаев Хамидулло Хабибуллаевич','Останов Фаррух Эркин ўғли','Саидов Аббосжон Абдуазиз ўғли','Сайфитдинов Баходир Нормахматович','Ахматханов Одилжон Акрам ўғли','Курбанов Файзулла Отаназарович','Каримов Тохиржон Дарибоевич','Жураев Ихтиёржон Адхамжонович','Зайитов Вохид Расулжонович','Михлиев Тўймурод Камолжон ўғли','Чутанов Абдували Некбаевич','Ибрагимов Дониёр Қурбаназарович','Жиянов Абдимўмин Тўраевич','Бекмуродов Озоджон Рўзивойжон ўғли','Давитов Нажмидин Райимович','Базаров Темур Бабажанович','Рустамов Шерзод Нормуминович','Султамуратов Жамбил Бахитжанович','Худайбергенова Нина Александровна','Рузметов Озод Пирметович']
    from django.utils.text import slugify
    for i in inspektorlar:
        username = slugify(i, allow_unicode=True)
        u = User(username=username.translate(tr), first_name=i)
        u.set_password('inspektor')
        u.save()
        u.groups.add(g)

    gi = Group.objects.create(name='inspeksiya')
    ui = User(username='inspeksiya', first_name="Inspeksiya")
    ui.set_password('123inspeksiya123')
    ui.save()
    ui.groups.add(gi)


    return HttpResponse("Yes")

@login_exempt
def login(request):
    if request.user.is_authenticated:
        if has_group(request.user, "inspektor"):
            return redirect("dalolatnoma_list")
        return redirect("index")

    if request.method == "POST":
        from django.contrib.auth import login, authenticate  # add this

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            if has_group(user, "inspektor"):
                return redirect("dalolatnoma_list")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout(request):
    from django.contrib.auth import logout

    logout(request)
    
    # messages.info(request, "You have successfully logged out.")
    return redirect("login")


@user_passes_test(lambda u: not has_group(u, 'inspektor'))
def index(request):
    import json
    main_data = "Gidromonitoring tizimi"
    
    # holat turlari bo'yicha yildagi oylik ma'lumotlar
    g1 = Dalolatnoma.objects.raw(
    """
SELECT 1 as id, n.nomi AS nomi, m.mon AS oy, Count(Date_part('month', d.korsatma_sana)) AS soni
FROM   (SELECT 1 AS mon        UNION ALL
        SELECT 2 AS mon        UNION ALL
        SELECT 3 AS mon        UNION ALL
        SELECT 4 AS mon        UNION ALL
        SELECT 5 AS mon        UNION ALL
        SELECT 6 AS mon        UNION ALL
        SELECT 7 AS mon        UNION ALL
        SELECT 8 AS mon        UNION ALL
        SELECT 9 AS mon        UNION ALL
        SELECT 10 AS mon       UNION ALL
        SELECT 11 AS mon       UNION ALL
        SELECT 12 AS mon) AS m
    CROSS JOIN monitoring_noqonuniy_holat_turi n
    LEFT JOIN monitoring_dalolatnoma d
            ON d.noqonuniy_holat_turi_id = n.id
                AND Date_part('year', d.korsatma_sana) =
                    Date_part('year', CURRENT_DATE)
                AND Date_part('month', d.korsatma_sana) = m.mon
GROUP  BY Date_part('month', d.korsatma_sana),n.nomi,m.mon
ORDER  BY nomi,oy    """
    )
    g2 = list(g1)
    def msum(spiska):
        sum=0
        for s in spiska:
            sum += s.soni
        return sum
    g2=({g2[x].nomi: [msum(g2[x: x+12]), int(x/12)] for x in range (0, len(g2),12)})

    #joriy yildagi oylar bo'yicha
    g3 = list(g1)
    g3=([[g3[x].nomi, [q.soni for q in g3[x: x+12]]] for x in range (0, len(g3),12)])

    # karta uchun
    # xarita = Dalolatnoma.objects.all()
    
    # inspektorlar bo'yicha
    cursor = connection.cursor()

    cursor.execute("""
SELECT n.nomi AS nomi, m.mon AS oy, sum(case
    when Date_part('month', d.korsatma_sana) isnull then 0
    else 1
    end) as soni ,  u.username as username, u.first_name as fn
FROM   (SELECT 1 AS mon        UNION ALL
        SELECT 2 AS mon        UNION ALL
        SELECT 3 AS mon        UNION ALL
        SELECT 4 AS mon        UNION ALL
        SELECT 5 AS mon        UNION ALL
        SELECT 6 AS mon        UNION ALL
        SELECT 7 AS mon        UNION ALL
        SELECT 8 AS mon        UNION ALL
        SELECT 9 AS mon        UNION ALL
        SELECT 10 AS mon       UNION ALL
        SELECT 11 AS mon       UNION ALL
        SELECT 12 AS mon) AS m
    CROSS JOIN monitoring_noqonuniy_holat_turi n
    CROSS JOIN auth_user u
    INNER JOIN auth_user_groups g on
                 g.user_id = u.id 
                   AND g.group_id = 2 

    LEFT JOIN monitoring_dalolatnoma d
            ON d.noqonuniy_holat_turi_id = n.id
                AND Date_part('year', d.korsatma_sana) =
                    Date_part('year', CURRENT_DATE)
                AND Date_part('month', d.korsatma_sana) = m.mon
                AND u.id = d.inspektor_id

    
--WHERE g.group_id = 2
--        n.id = 1
                   
GROUP  BY  n.nomi, m.mon, u.id
-- ORDER  BY n.nomi desc,oy
ORDER  BY u.username, oy, n.nomi asc
                       """)
    _inspektorlar_kesimida = cursor.fetchall()


    udict = {}
    for (nht, oy, soni,  username, fn) in _inspektorlar_kesimida:
        if username in udict:
            if nht in udict[username]:
                udict[username][nht].append([oy, soni])
            else:
                udict[username].update({nht: [[oy, soni]]}) 
        else:
            udict[username] = {nht: [[oy, soni]]}

    # pprint(udict)
    # Umumiy respublikada, 
    # Viloyatlar kesimida (har bir nht bo'yicha, oy bo'yicha)

    cursor = connection.cursor()

    cursor.execute("""
SELECT n.nomi AS nomi, m.mon AS oy, sum(case
    when Date_part('month', d.korsatma_sana) isnull then 0
    else 1
    end) as soni ,  v.nomi as viloyat
FROM   (SELECT 1 AS mon        UNION ALL
        SELECT 2 AS mon        UNION ALL
        SELECT 3 AS mon        UNION ALL
        SELECT 4 AS mon        UNION ALL
        SELECT 5 AS mon        UNION ALL
        SELECT 6 AS mon        UNION ALL
        SELECT 7 AS mon        UNION ALL
        SELECT 8 AS mon        UNION ALL
        SELECT 9 AS mon        UNION ALL
        SELECT 10 AS mon       UNION ALL
        SELECT 11 AS mon       UNION ALL
        SELECT 12 AS mon) AS m
    CROSS JOIN monitoring_noqonuniy_holat_turi n
    CROSS JOIN monitoring_tuman t
    INNER JOIN monitoring_viloyat v on
                 t.viloyat_id = v.id

    LEFT JOIN monitoring_dalolatnoma d
            ON d.noqonuniy_holat_turi_id = n.id
                AND Date_part('year', d.korsatma_sana) =
                    Date_part('year', CURRENT_DATE)
                AND Date_part('month', d.korsatma_sana) = m.mon
                AND d.tuman_id = t.id
    
--WHERE --m.mon = 3
--        n.id = 1
                   
GROUP  BY  n.nomi, m.mon, v.id
-- ORDER  BY n.nomi desc,oy
ORDER  BY v.id, oy, n.nomi asc
                       """)
    _viloyatlar_kesimida = cursor.fetchall()


    vdict = {}
    for (nht, oy, soni, viloyat) in _viloyatlar_kesimida:
        if viloyat in vdict:
            if nht in vdict[viloyat]:
                vdict[viloyat][nht].append([oy, soni])
            else:
                vdict[viloyat].update({nht: [[oy, soni]]}) 
        else:
            vdict[viloyat] = {nht: [[oy, soni]]}

    nhtlar = Noqonuniy_holat_turi.objects.all().order_by('nomi')

    # viloyatlar_kesimida = []
    # for q in range(0, len(_viloyatlar_kesimida), len(nhtlar)):
    #     _nhtlar = []
    #     for i in range(len(nhtlar)):
    #         _nhtlar.append(_viloyatlar_kesimida[i][0])
    #     viloyatlar_kesimida.append([_viloyatlar_kesimida[q][1], _viloyatlar_kesimida[q][2],_viloyatlar_kesimida[q][3],_nhtlar])

    # pprint(viloyatlar_kesimida)
    # pprint(len(viloyatlar_kesimida))

    data = {
        "main_text": main_data,
        'g1': g1,
        'g3': json.dumps(g3),
        'g2': g2,
        # 'xarita':list(xarita),
        'vdict':vdict,
        'udict':udict,
        'nhtlar':nhtlar,
    }
    return render(request, "index.html", context=data)

def xarita_from_to(request):
    sanadan = request.POST.get('sanadan', None)
    sanagacha = request.POST.get('sanagacha', None)
    p_holati = request.POST.get('holati', None)
    p_viloyat = request.POST.get('viloyat', None)
    p_inspektor = request.POST.get('inspektor', None)
    p_nht = request.POST.get('nht', None)
    xarita = Dalolatnoma.objects
    if sanadan:
        xarita=xarita.filter(korsatma_sana__gte=sanadan)
    if sanagacha:
        xarita=xarita.filter(korsatma_sana__lte=sanagacha)
    # xarita=xarita.all()
    if (has_group( request.user, 'inspektor')):
        xarita=xarita.filter(inspektor=request.user)

    if p_viloyat:
        p_viloyat = int(p_viloyat)
        xarita=xarita.filter(tuman__viloyat_id=p_viloyat)
    if p_inspektor:
        p_inspektor = int(p_inspektor)
        xarita=xarita.filter(inspektor__id=p_inspektor)
    if p_holati:
        p_holati = False if p_holati=='0' else True
        xarita=xarita.filter(bartaraf_etilganligi=p_holati)
    if p_nht:
        p_nht = int(p_nht)
        xarita=xarita.filter(noqonuniy_holat_turi__id=p_nht)


    xarita=xarita.all() 
    xarita = [{'pk':x.pk, 'bartaraf_etilganligi':x.bartaraf_etilganligi, 'bartaraf_etilmagan':x.bartaraf_etilmagan, 'lat':x.lat,'lng':x.lng, 'korsatma_raqam':x.korsatma_raqam, 'created_at':x.created_at} for x in xarita]
    return JsonResponse({"xarita": xarita}) 

def tuman_list(request):
    id_viloyat = request.POST.get('idv')
    tumanlar = Tuman.objects.filter(viloyat_id=id_viloyat).order_by('nomi').values_list('pk', 'nomi')
    tumanlar = list(tumanlar)
    return JsonResponse({"tumanlar": tumanlar}) 

def stansiya_seriya(request):
    id_stansiya = request.POST.get('stansiya')
    seriya = Stansiya.objects.filter(pk=id_stansiya).first().seriya
    return JsonResponse({"seriya": seriya}) 

def export_to_excel(request, queryset):
    from openpyxl.styles import Font
    from openpyxl import Workbook
    from datetime import datetime
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="gidromonitoring_'+datetime.now().strftime("%Y.%m.%d")+'.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Noqonuniy holatlar"

    # Add headers
    headers = ["№    ","Noqonuniy holat turi", "Huquqbuzar turi", "Huquqbuzar nomi", "Huquqbuzar STIR",
               "Viloyat", "Tuman", "Orientir", "Stansiya", "Inspektor", "Korsatma", 
               "Sana", "Amal qilish muddati", "Bartaraf etilganligi"]
    ws.append(headers)

    for i, obj in enumerate( queryset):
        ws.append([i, obj.noqonuniy_holat_turi.nomi, obj.huquqbuzar_turi, obj.huquqbuzar_nomi, obj.huquqbuzar_stir,
                   obj.tuman.nomi, obj.tuman.viloyat.nomi, obj.orientir, obj.stansiya.nomi, obj.inspektor.first_name if obj.inspektor.first_name else obj.inspektor.username,
                   obj.korsatma_raqam, str(obj.korsatma_sana), str(obj.amal_qilish_muddati), "Bartaraf etilgan" if obj.bartaraf_etilganligi is True else "Bartaraf etilgaman"])

    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length

    header_font = Font(bold=True)
    for cell in ws["1:1"]:
        cell.font = header_font

    wb.save(response)
    return response

def dalolatnoma_list(request):
    queryset = Dalolatnoma.objects.select_related("tuman__viloyat", 'noqonuniy_holat_turi', 'stansiya', 'inspektor').all().order_by('-korsatma_sana')
    viloyatlar = Viloyat.objects.all()
    nhtlar = Noqonuniy_holat_turi.objects.all()
    inspektorlar = User.objects.filter(groups__name='inspektor').order_by('first_name').all()

    if (has_group(request.user, 'inspektor')):
        queryset = queryset.filter(inspektor=request.user)

    page = request.GET.get('page', 1)

    p_sana1 = request.GET.get('sana1', None)
    p_sana2 = request.GET.get('sana2', None)

    p_viloyat = request.GET.get('viloyat', None)
    p_nht = request.GET.get('nht', None)
    p_inspektor = request.GET.get('inspektor', None)
    p_bartaraf = request.GET.get('bartaraf_etilganligi', None)
    p_query = ''
    if p_sana1:
        p_query += '&sana1='+p_sana1
        queryset = queryset.filter(korsatma_sana__gte=p_sana1)
    if p_sana2:
        p_query += '&sana2='+p_sana2
        queryset = queryset.filter(korsatma_sana__lte=p_sana2)
    if p_viloyat:# is not None or len(p_viloyat)>0:
        p_query += '&viloyat='+p_viloyat
        p_viloyat = int(p_viloyat)
        queryset = queryset.filter(tuman__viloyat_id=p_viloyat)
    if p_inspektor:
        p_query += '&inspektor='+p_inspektor
        p_inspektor = int(p_inspektor)
        queryset = queryset.filter(inspektor__id=p_inspektor)
    if p_bartaraf:
        p_query += '&bartaraf_etilganligi='+p_bartaraf
        p_bartaraf = False if p_bartaraf=='0' else True
        queryset = queryset.filter(bartaraf_etilganligi=p_bartaraf)
    if p_nht:
        p_query += '&nht='+p_nht
        p_nht = int(p_nht)
        queryset = queryset.filter(noqonuniy_holat_turi__id=p_nht)

    if request.method == 'POST':
        excel = request.POST.get('excel')
        if excel=="1":
            return export_to_excel(request, queryset)
    paginator = Paginator(queryset, 20)
    count_all = queryset.count()
    count_done = queryset.filter(bartaraf_etilganligi=True).count()

    from datetime import date

    count_failed = queryset.filter(bartaraf_etilganligi=False, amal_qilish_muddati__lt=date.today()).count()
    count_progress = count_all-count_done-count_failed
    try:
        dlist = paginator.page(page)
    except PageNotAnInteger:
        dlist = paginator.page(1)
    except EmptyPage:
        dlist = paginator.page(paginator.num_pages)

    return render(request, 'dalolatnoma_list.html', {'dlist': dlist,
                                                    'viloyatlar':viloyatlar,
                                                    'nhtlar':nhtlar,
                                                    'inspektorlar':inspektorlar,
                                                    'p_sana1':p_sana1,
                                                    'p_sana2':p_sana2,
                                                    'p_viloyat':p_viloyat,
                                                    'p_inspektor':p_inspektor,
                                                    'p_bartaraf':p_bartaraf,
                                                    'p_nht':p_nht,
                                                    'p_query':p_query,
                                                    'count_all':count_all,
                                                    'count_done':count_done,
                                                    'count_progress':count_progress,
                                                    'count_failed':count_failed,
                                                    })

def dalolatnoma_one(request, id):
    dalolatnoma = get_object_or_404(Dalolatnoma.objects.select_related("tuman__viloyat", 'noqonuniy_holat_turi', 'stansiya', 'inspektor').prefetch_related('dalolatnomarasm_set'), pk=id)
    return render(request, "dalolatnoma_one.html", {'d':dalolatnoma})

def dalolatnoma_edit(request, id):
    dalolatnoma = get_object_or_404(Dalolatnoma.objects.select_related("tuman__viloyat", 'noqonuniy_holat_turi', 'stansiya', 'inspektor').prefetch_related('dalolatnomarasm_set'), pk=id)
    dform = DalolatnomaForm(instance=dalolatnoma)
    return render(request, 'dalolatnoma_edit.html', {'d_form':dform,'d':dalolatnoma})

@user_passes_test(lambda u: not has_group(u, 'inspeksiya'))
def dalolatnoma_new(request):
    dform = DalolatnomaForm()
    
    if request.method == 'POST':
        
        k_qogoz = request.FILES.get('korsatma_rasm_qogoz')
        k_odam = request.FILES.get('korsatma_rasm_odam')
        rasmlar = request.FILES.getlist('rasmlar[]')
        dform = DalolatnomaForm(request.POST, request.FILES)
        stansiya_prefix = Stansiya.objects.filter(pk=dform.data['stansiya']).first().seriya
        dform.data._mutable = True
        dform.data['korsatma_raqam'] = stansiya_prefix + dform.data['korsatma_raqam']
        dform.data._mutable = False

        if dform.is_valid():
            dalolatnoma = dform.save(commit=False)
            dalolatnoma.inspektor = request.user
            dalolatnoma.save()
            messages.success(request, "Dalolatnoma created successfully")
            
            for file in rasmlar:
                DalolatnomaRasm.objects.create(dalolatnoma=dalolatnoma, rasm=file)
            storage = messages.get_messages(request)
            storage.used = True
            return JsonResponse({"message": "Bexato"})
            
        return JsonResponse({"message": "Xato", "errors": dform.errors.as_json()})
    
    context = {"d_form": dform}
    return render(request, "dalolatnoma_new.html", context)

@user_passes_test(lambda u: not has_group(u, 'inspektor'))
def dalolatnoma_bartaraf_etildi(request, id):
    dalolatnoma = get_object_or_404(Dalolatnoma.objects, pk=id)
    try:
        brt_file = request.FILES.get('file')
        dalolatnoma.bartaraf_etilganligi_hujjati=brt_file
        dalolatnoma.bartaraf_etilganligi_hujjati_sana = datetime.datetime.today()
        dalolatnoma.save()
        messages.info(request, "Bartaraf etilganligi hujjati saqlandi.")
    except:
        messages.error(request, "Bartaraf etilganligi hujjatini saqlashda xatolik.")
    return redirect('dalolatnoma_list')

@user_passes_test(lambda u: not has_group(u, 'inspektor') and not has_group(u, 'inspeksiya'))
def dalolatnoma_bartaraf_etildi_admin(request, id):
    dalolatnoma = get_object_or_404(Dalolatnoma.objects, pk=id)
    try:
        dalolatnoma.bartaraf_etilganligi = True
        dalolatnoma.bartaraf_etilganligi_sana = datetime.datetime.today()
        # print(dalolatnoma)
        dalolatnoma.save()
    except:
        messages.error(request, "Bartaraf etilganligi saqlashda xatolik.")
    return redirect('dalolatnoma_list')





@user_passes_test(lambda u: not has_group(u, 'inspeksiya'))
def dalolatnoma_new_checkbox(request):
    dform = DalolatnomaForm()
    
    if request.method == 'POST':
        
        k_qogoz = request.FILES.get('korsatma_rasm_qogoz')
        k_odam = request.FILES.get('korsatma_rasm_odam')
        rasmlar = request.FILES.getlist('rasmlar[]')
        nhtlar = request.POST.getlist('noqonuniy_holat_turi')
        krr = request.POST.get('korsatma_raqam')
        birinchi = False
        if len(nhtlar)==0:
            dform = DalolatnomaForm(request.POST, request.FILES)
            # dform.add_error('noqonuniy_holat_turi', "Birorta noqonuniy holat tanlanishi kerak!")
            return JsonResponse({"message": "Xato", "errors": dform.errors.as_json()})

        # birinchisini saqlab qolganlarni shuni kopiyasini yaratish pk=NULL keyin save()
        for i in range(len(nhtlar)):
            print(nhtlar[i])
            request.POST._mutable = True
            request.POST['noqonuniy_holat_turi']=nhtlar[i]
            request.POST._mutable = False
            dform = DalolatnomaForm(request.POST, request.FILES)
            stansiya_prefix = Stansiya.objects.filter(pk=dform.data['stansiya']).first().seriya
            kr0 = stansiya_prefix + krr
            if (len(nhtlar)>1):
                kr = kr0 + "-" + str(i+1)
            else: 
                kr = kr0
            dform.data._mutable = True
            dform.data['korsatma_raqam'] = kr
            dform.data._mutable = False
            if birinchi == False:
                birinchi=True
                if dform.is_valid():
                    dalolatnoma = dform.save(commit=False)
                    dalolatnoma.inspektor = request.user
                    dalolatnoma.save()
                    messages.success(request, "Dalolatnoma created successfully")
                    
                    for file in rasmlar:
                        DalolatnomaRasm.objects.create(dalolatnoma=dalolatnoma, rasm=file)
                    storage = messages.get_messages(request)
                    storage.used = True
                else:
                    print(dform.errors)
                    return JsonResponse({"message": "Xato", "errors": dform.errors.as_json()})
            else:
                drs = DalolatnomaRasm.objects.filter(dalolatnoma=dalolatnoma).all()
                print(drs)
                nextd = dalolatnoma
                nextd.pk = None
                nextd.korsatma_raqam = kr
                nextd.noqonuniy_holat_turi=Noqonuniy_holat_turi.objects.filter(pk=nhtlar[i]).first()
                nextd.save()
                for dr in drs:
                    dr.pk=None
                    dr.dalolatnoma=nextd
                    print(dr)
                    print("=========================")
                    dr.save()

        return JsonResponse({"message": "Bexato"})
    
    context = {"d_form": dform}
    return render(request, "dalolatnoma_new_checkbox.html", context)
