from db_helper import query_table
import xlsxwriter
import pandas as pd


def write_portfolio_details(report_name):

    output_file_name = report_name

    sheet_2_name = 'Positions details'
    sheet_name = 'Portfolio details'

    writer = pd.ExcelWriter(output_file_name, engine='xlsxwriter')

    data_portfolio = query_table('select * from portfolio')
    data_positions = query_table('select * from positions')

    # Convert the dataframe to an XlsxWriter Excel object.
    data_portfolio.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)

    data_positions.to_excel(writer, sheet_name=sheet_2_name, startrow=1, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    worksheet2 = writer.sheets[sheet_2_name]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = data_portfolio.shape

    # Create a list of column headers, to use in add_table().
    column_settings = []
    for header in data_portfolio.columns:
        column_settings.append({'header': header})

    # Add the table.
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    #positions
    (max_row, max_col) = data_positions.shape
    column_settings = []
    for header in data_positions.columns:
        column_settings.append({'header': header})
    worksheet2.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
    worksheet2.set_column(0, max_col - 1, 12)

    chart = workbook.add_chart({'type': 'line'})

    chart.add_series({
        'values': f"=\'{sheet_name}\'!$D$2:$D$25",
        "name": "PnL",
        'categories': f"=\'{sheet_name}\'!$A$2:$A$25"
    })

    worksheet.insert_chart('G4', chart)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
