from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from bot.db.crud.visit_crud import visit_crud
from bot.db.models.users import User
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from sqlalchemy.ext.asyncio import AsyncSession

# TODO доработать посещения
def pdf_report(users: User, visits):
    n=20
    vis = 0
    c = canvas.Canvas(f'report.pdf',pagesize=A4, bottomup=0)
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    c.setLineWidth(2)
    c.setFont('Arial',size=10)
    c.drawString(20,n,text=f'ФИО')
    c.drawString(220,n,text=f'Номер')
    c.drawString(345,n,text=f'Бонусы')
    c.drawString(425,n,text=f'Посещения')
    c.line(20,n+5,550,n+5)
    n+=20
    for user in users:
        for visit in visits:
            if user.id == visits.user_id:
                vis+=1
            
        c.drawString(20,n,text=f'{user.last_name} {user.first_name}')
        c.drawString(220,n,text=f'{user.phone_number}')
        c.drawString(345,n,text=f'{user.balance}')
        c.drawString(425,n,text=f'{vis}')
        c.line(20,n+5,550,n+5)
        vis = 0
        n+=20
        if n%800==0:
            c.showPage()
            n=20
            c.setLineWidth(2)
            c.setFont('Arial',size=10)
            c.drawString(20,n,text=f'ФИО')
            c.drawString(220,n,text=f'Номер')
            c.drawString(345,n,text=f'Бонусы')
            c.line(20,n+5,550,n+5)
            n+=20
            
    c.save()
    
# TODO не запускал, работоспособность неизвестна
def pdf_report_for_unit(users: User, visits, unit):
    n=20
    vis = 0
    c = canvas.Canvas(f'report.pdf',pagesize=A4, bottomup=0)
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    c.setLineWidth(2)
    c.setFont('Arial',size=10)
    c.drawString(20,n,text=f'Дата')
    c.drawString(220,n,text=f'ФИО Админа')
    c.drawString(345,n,text=f'Услуги')
    c.drawString(425,n,text=f'Сумма оплаты')
    c.line(20,n+5,550,n+5)
    n+=20
    for user in users:
        for visit in visits:
            if user.business_unit_id == unit.id:
                vis+=1
            
        c.drawString(20,n,text=f'{visit.date}')
        c.drawString(220,n,text=f'{user.last_name} {user.first_name}')
        c.drawString(345,n,text=f'{visit.service_id}')
        c.drawString(425,n,text=f'{visit.summ}')
        c.line(20,n+5,550,n+5)
        vis = 0
        n+=20
        if n%800==0:
            c.showPage()
            n=20
            c.setLineWidth(2)
            c.setFont('Arial',size=10)
            c.drawString(20,n,text=f'ФИО')
            c.drawString(220,n,text=f'Номер')
            c.drawString(345,n,text=f'Бонусы')
            c.line(20,n+5,550,n+5)
            n+=20
            
    c.save()
    

def report_info_client_for_admin(user: User,visits, session: AsyncSession):
    n=20
    c = canvas.Canvas(f'report.pdf', pagesize=A4, bottomup=0)
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    c.setLineWidth(2)
    c.setFont('Arial',size=10)
    c.drawString(20,n,text=f'ФИО')
    c.drawString(220,n,text=f'Номер')
    c.drawString(345,n,text=f'Дата рождения')
    c.drawString(425,n,text=f'Бонусы')
    c.line(20,n+5,550,n+5)
    n+=20
    c.drawString(20,n,text=f'{user.last_name} {user.first_name}')
    c.drawString(220,n,text=f'{user.phone_number}')
    c.drawString(345,n,text=f'{user.birth_date}')
    c.drawString(425,n,text=f'{user.balance}')
    c.line(20,n+5,550,n+5)
    n+=60
    c.setFont('Arial',size=8)
    c.drawString(20,n,text=f'Дата посещения')
    c.drawString(120,n,text=f'Бизнес-юнит')
    c.drawString(210,n,text=f'ФИО админа')
    #c.drawString(300,n,text=f'Услуги')
    c.drawString(390,n,text=f'Сумма ')
    #c.drawString(470,n,text=f'Начисление\списание')
    c.line(20,n+5,550,n+5)
    n+=20
    
    for visit in visits:
        #bonus = user.bonuses
        c.drawString(20,n,text=f'{visit.date}')
        c.drawString(120,n,text=f'{visit.business_unit.name}')
        c.drawString(210,n,text=f'{visit.admin_user.last_name} {visit.admin_user.first_name}')
        c.drawString(390,n,text=f'{visit.summ}')
        #c.drawString(470,n,text=f'{bonus}')
        c.line(20,n+5,550,n+5)
        n+=20
        if n%800==0:
            c.showPage()
            n=20
            c.setLineWidth(2)
            c.setFont('Arial',size=8)
            c.drawString(20,n,text=f'Дата посещения')
            c.drawString(120,n,text=f'Бизнес-юнит')
            c.drawString(210,n,text=f'ФИО админа')
            #c.drawString(300,n,text=f'Услуги')
            c.drawString(390,n,text=f'Сумма ')
            #c.drawString(470,n,text=f'Начисление\списание')
            c.line(20,n+5,550,n+5)
            n+=20
        
    c.save()