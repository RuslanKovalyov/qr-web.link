from django.shortcuts import render
import qrcode
from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='Enter URL')

    def generate_qr(self):
        url = self.cleaned_data['url']
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="#F5E216")
        return img

def generate_qr(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            img = form.generate_qr()
            img.save("static/qr.png")
            img.save("main/static/qr.png")
            return render(request, 'qr.html')
        else:
            error_message = "Please enter a valid URL."
            return render(request, 'input_url.html', {'form': form, 'error_message': error_message})
    else:
        form = URLForm()
    return render(request, 'input_url.html', {'form': form})
