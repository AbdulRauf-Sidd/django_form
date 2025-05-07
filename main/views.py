from django.shortcuts import render, redirect
from .forms import FinancialDataForm
from django.conf import settings
from django.core.files.storage import default_storage
import os
from datetime import datetime
from .helpers import upload_to_r2, construct_path, compile_content_name, construct_event, append_event_to_json

def financial_data_view(request):
    if request.method == 'POST':
        form = FinancialDataForm(request.POST, request.FILES)
        if form.is_valid():
            ticker = form.cleaned_data.get("equity")
            quarter = form.cleaned_data.get("quarter")
            year = form.cleaned_data.get("year")
            published_date = form.cleaned_data.get("published_date")
            fiscal_date = form.cleaned_data.get("fiscal_date")
            file = form.cleaned_data['file']
            file_path = default_storage.save(file.name, file)
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

            # published_date = datetime.strptime(str(published_date), "%Y-%m-%d")

            # Format the date object into the desired string format
            # published_date = published_date.strftime('%Y-%m-%d')

            # if fiscal_date:
            #     fiscal_date = datetime.strptime(str(fiscal_date), "%Y-%m-%d")
                # Format the date object into the desired string format
                # fiscal_date = fiscal_date.strftime('%Y-%m-%d')

            # You can now use `full_file_path` for further processing
           
            if quarter != 4 and quarter is not None:
                content_type = "quarterly_report"
                periodicity = "periodic"
            elif quarter == 4:
                content_type = "annual_report"
                periodicity = "periodic"
            else:
                content_type = None
                periodicity = "non-periodic"
            geography = "us"
            content_name = compile_content_name(content_type, ticker, year, quarter)
            file_type = 'pdf'
            file_name = file.name
            path = construct_path(ticker, published_date, file_name)
            r2_url = upload_to_r2(full_file_path, file_name, path, True)

            if year:
                year = int(year)
            if quarter:
                quarter = int(quarter)

            event = construct_event(
                equity_ticker=ticker,
                content_name=content_name,
                content_type=content_type,
                published_date=str(published_date),
                r2_url=r2_url,
                periodicity=periodicity,
                file_type=file_type,
                geography=geography,
                fiscal_date=str(fiscal_date),
                fiscal_year=year,
                fiscal_quarter=quarter
            )

            append_event_to_json(event)
   

            # Process the form data (e.g., save to database)
            # For now, we'll just refresh the page
            return redirect('financial_data')
        else:
            # If the form is not valid, render the form with error messages
            return render(request, 'financial_data.html', {'form': form})
    else:
        form = FinancialDataForm()
    return render(request, 'financial_data.html', {'form': form})
