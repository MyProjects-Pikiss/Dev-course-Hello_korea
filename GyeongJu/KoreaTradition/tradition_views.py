from django.shortcuts import render, redirect
from .models import *
from .experience_constant import *
from django.views.decorators.csrf import csrf_exempt
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hello_Korea.settings")
django.setup()
from GyeongJu.models import hard_coded_text

@csrf_exempt
def tradition_view(request):
    typename = TypeInfo.objects.get(type='전통문화체험')
    if request.method == 'POST':
        cur_lang = request.POST['select_language']
        LanguageInfo.objects.filter(selected=True).update(selected=False)
        LanguageInfo.objects.filter(lang=cur_lang).update(selected=True)
        language = LanguageInfo.objects.all()
        form_text = Tradition_form.objects.filter(lang=cur_lang).first()
        text_data=hard_coded_text.objects.filter(lang = cur_lang).first()
        data = TraditionExperienceInfo.GetInfoByLangType(type_name=typename, language=cur_lang)
        return render(request, 'GyeongJu/tradition/index.html', {'data': data, 'type': form_text.koreaTradition, 'language': language, 'form_text':form_text, 'hard_coded': text_data})
    else:
        get_lang = LanguageInfo.GetCurrentLanguage().lang
        language = LanguageInfo.objects.all()
        form_text = Tradition_form.objects.filter(lang=get_lang).first()
        text_data=hard_coded_text.objects.filter(lang = get_lang).first()
        data = TraditionExperienceInfo.GetInfoByLangType(type_name=typename, language=get_lang)
        return render(request, 'GyeongJu/tradition/index.html', {'data': data, 'type': form_text.koreaTradition, 'language': language, 'form_text':form_text, 'hard_coded': text_data})

@csrf_exempt
def clothes_view(request):
    typename = TypeInfo.objects.get(type='의복체험')
    if request.method == 'POST':
        cur_lang = request.POST['select_language']
        LanguageInfo.objects.filter(selected=True).update(selected=False)
        LanguageInfo.objects.filter(lang=cur_lang).update(selected=True)
        language = LanguageInfo.objects.all()
        form_text = Tradition_form.objects.filter(lang=cur_lang).first()
        text_data=hard_coded_text.objects.filter(lang = cur_lang).first()
        data = TraditionExperienceInfo.GetInfoByLangType(type_name=typename, language=cur_lang)
        return render(request, 'GyeongJu/tradition/index.html', {'data': data, 'type': form_text.clothTradition, 'language': language, 'form_text':form_text, 'hard_coded': text_data})
    else:
        get_lang = LanguageInfo.GetCurrentLanguage().lang
        language = LanguageInfo.objects.all()
        form_text = Tradition_form.objects.filter(lang=get_lang).first()
        text_data=hard_coded_text.objects.filter(lang = get_lang).first()
        data = TraditionExperienceInfo.GetInfoByLangType(type_name=typename, language=get_lang)
        return render(request, 'GyeongJu/tradition/index.html', {'data': data, 'type': form_text.clothTradition, 'language': language, 'form_text':form_text, 'hard_coded': text_data})

@csrf_exempt
def accomodation_view(request):
    typename = TypeInfo.objects.get(type='고택체험')
    if request.method == 'POST':
        cur_lang = request.POST['select_language']
        LanguageInfo.objects.filter(selected=True).update(selected=False)
        LanguageInfo.objects.filter(lang=cur_lang).update(selected=True)
        language = LanguageInfo.objects.all()
        form_text = Tradition_form.objects.filter(lang=cur_lang).first()
        text_data=hard_coded_text.objects.filter(lang = cur_lang).first()
        data = TraditionExperienceInfo.GetInfoByLangType(type_name=typename, language=cur_lang)
        return render(request, 'GyeongJu/tradition/index.html', {'data': data, 'type': form_text.lodgeTradition, 'language': language, 'form_text':form_text, 'hard_coded': text_data})
    else:
        get_lang = LanguageInfo.GetCurrentLanguage().lang
        language = LanguageInfo.objects.all()
        form_text = Tradition_form.objects.filter(lang=get_lang).first()
        text_data=hard_coded_text.objects.filter(lang = get_lang).first()
        data = TraditionExperienceInfo.GetInfoByLangType(type_name=typename, language=get_lang)
        return render(request, 'GyeongJu/tradition/index.html', {'data': data, 'type': form_text.lodgeTradition, 'language': language, 'form_text':form_text, 'hard_coded': text_data})
