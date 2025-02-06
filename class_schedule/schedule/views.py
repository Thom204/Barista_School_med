import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .sheets_service import read_schedule, write_class, delete_class, get_service, update_class_students
from .models import Clase
from datetime import datetime, timedelta

# Create your views here.
def list_classes(request):
    clases = read_schedule()
    return render(request, "schedule/list.html", {"clases": clases})

def create_class(request):
    if request.method == "POST":
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        profesores = request.POST.getlist("profesores")
        alumnos = request.POST.getlist("alumnos")

        # Validaciones: Debe haber al menos 2 profesores y 4 alumnos
        if len(profesores) < 2:
            return render(request, "schedule/create.html", {"error": "Debe haber al menos 2 profesores."})
        if len(alumnos) > 4:
            return render(request, "schedule/create.html", {"error": "Una clase tiene como maximo 4 alumnos."})
        
        if fecha=='' or hora=='':
            return render(request, "schedule/create.html", {"error": "Seleccione un horario"})
        
        col = int(datetime.strptime(request.POST["fecha"], "%Y-%m-%d").weekday()) +1
        

        try:
            # Guardamos en la BD
            clase = Clase(
                fecha=fecha,
                hora=hora,
                profesores=json.dumps(profesores),  # Guardar como JSON
                alumnos=json.dumps(alumnos)  # Guardar como JSON
            )
            clase.save()

            # Guardamos en Google Sheets
            write_class(col, clase)
            return redirect("list_classes")
        
        except ValueError as e:
            return render(request, "schedule/create.html", {"error": str(e)})

    return render(request, "schedule/create.html")

def delete_class_view(request, row, col):
    delete_class(row, col)
    return redirect("list_classes")

def search_classes(request):
    if request.method == "GET":
        week_start = request.GET.get("week_start")
        if week_start:
            week_start_date = datetime.strptime(week_start, "%Y-%m-%d")
            week_end_date = week_start_date + timedelta(days=7)
            clases = [clase for clase in read_schedule() if week_start_date.strftime("%Y-%m-%d") <= clase["fecha"] <= week_end_date.strftime("%Y-%m-%d")]
            return render(request, "schedule/search.html", {"clases": clases})
    return render(request, "schedule/search.html")


def editar_estudiantes(request):
    row = int(request.POST.get("row"))
    col = int(request.POST.get("col"))

    delete_class(row,col)
    return redirect("list_classes")
