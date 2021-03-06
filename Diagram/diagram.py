import matplotlib.pyplot as pyplot
from SQL import querys as sql
from Diagram import hex_converting
import seaborn as sb
import numpy as np
import pandas as ps
import sqlite3
import time
import config
from Diagram import weekly


__databaseFile = config.CONFIG['database_file_name']
sb.set(style="whitegrid")
save_plots = 'plots/'



# connect the sqllite database and return connection
def create_diagrams():
    connection = sqlite3.connect(__databaseFile)
    diagram_history_op_return(connection)
    diagram_content_OP_RETURN(connection)
    weekly.diagram_weekly()

# create a chart showing the use of the OP_RETURN field in relation to time
def diagram_history_op_return (connection):
    # create dataframe by using pandas with corresponding SQL statement and the connection to database
    read_data = ps.read_sql_query(sql.get_count_number_of_op_return(), connection)
    
    # get corresponding columns for the axes
    data = ps.DataFrame(read_data,columns=['create_date','Count_Duplicate'])
    data=data.rename(columns = {'create_date':'year'}) 
    data=data.rename(columns = {'Count_Duplicate':'transaction'}) 
    # x-axis: get create_date of blocks that ar containing OP_RETURNS in datetime 
    x_val = ps.Series(ps.to_datetime(data['year']))
    # y-axis: get number of OP_RETURNS in a Block depending on create_date as an array
    y_val = np.array(data['transaction'])

    # bulid with the values for x and y an series for plotting 
    s = ps.Series(y_val, index=x_val)
    # plot line diagram with corresponing x and y values and show it
    pyplot.ylim([0, np.max(y_val)+200])
    pyplot.margins(x=0)
    s.plot(color='#2A649F',label='All OP_RETURN Transactions')

    # store current diagram, show it, store it as file and close it for drawing other diagrams
    fig1 = pyplot.gcf()
    pyplot.ylabel('transaction')
    pyplot.show()
    pyplot.margins(x=0)
    pyplot.draw()
    fig1.savefig(save_plots+'time_line.png', dpi=1000)
    fig1.savefig(save_plots+'time_line.pdf', dpi=1000)
    pyplot.close()


# create a chart showing the content of the OP_RETURN fields in relation to number of the content
def diagram_content_OP_RETURN (connection):
    # create dataframe by using pandas with corresponding SQL statement and the connection to database
    read_data = ps.read_sql_query(sql.get_rmv_op_and_analyze_hex(), connection)
    # put values in data frame in an array
    list_str_op_retrun = np.array(read_data)
    # values for diagram with content of OP_RETURN an number of different contents
    result_array = analyze_op_hex(list_str_op_retrun)
    # get object for y-axisl    
    x_val = [x for x,_ in result_array]
    # get values for x-axis
    y_val = [y for _,y in result_array]
    #plot bar chart with corresponing x and y values and show it
    dia = sb.barplot(x=x_val,y= y_val, palette="rocket")
    dia.set_xticklabels(fontsize = 7, labels=x_val, rotation=26, ha='right')
    # store current diagram, show it, store it as file and close it for drawing other diagrams
    fig2 = pyplot.gcf()
    pyplot.show()
    pyplot.draw()
    fig2.savefig(save_plots+'category_bar_chart.png', dpi = 1000)
    fig2.savefig(save_plots+'category_bar_chart.pdf', dpi = 1000)
    pyplot.close()



# funtion to analyse the op-return content
def analyze_op_hex (op_array):
    #analyze the hex strings
    check_hex = (hex_converting.check_hex(op_array.tolist()))
    # return a list with number of different OP_RETURN field contents
    return check_hex
   

