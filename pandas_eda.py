

#Import the needed modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mpl_dates

#load the datasets as pandas dataframes
ls_roi_df = pd.read_csv('./data/bb_roi_ls5-9.csv')
ls_polys_df = pd.read_csv('./data/bb_polygons_ls4-9.csv')
sl_roi_df = pd.read_csv('./data/bb_roi_sl2.csv')
sl_polys_df = pd.read_csv('./data/bb_polygon_sl1.csv')

# print(sl_roi_df)

#make the generic scatter plots


# sl_roi_df.plot(x='Date', y='NDVI', kind='scatter')
# plt.show()

#=======================================================================================================================


#-----------------------------------------------------------------------------------------------------------------------
#I wiant to be able to extract specific months and plot those
#I will check the data type of the date field
# print(sl_roi_df['Date'].dtype)

#I will convert it to a datetime field
sl_roi_df["Date"] = pd.to_datetime(sl_roi_df["Date"])
# print(sl_roi_df['Date'].dtype)
#It worked

#extract the month and the year from the tables and make them into new columns
sl_roi_df['MonthNum'] = sl_roi_df['Date'].dt.month
sl_roi_df['YearNum'] = sl_roi_df['Date'].dt.year

# print(sl_roi_df)
# print(len(sl_roi_df.index))

#-----------------------------------------------------------------------------------------------------------------------
# I want to plot specific months
#have to drop the unnecessary months, or make a new dataframe
# I will look from May to September (5 months)



#drop the months thatdont meet the criteria
# df2 = sl_roi_df[sl_roi_df.MonthNum >= 5]
# print(df2, '\n', len(df2.index))
# df2 = df2[df2.MonthNum <= 9]
# print(df2, '\n', len(df2.index))



#=======================================================================================================================
#                   1. Functions
#=======================================================================================================================

#function to add a year and month column
def add_year_and_month(df, dt_column):
    """
    adds a year a month column from a date column
    :param df: pandas dataframe
    :param dt_column: the month column; string
    :return: dataframe
    """
    #check if the column is a datetime type
    if(df[dt_column].dtype == 'datetime64'):
        pass
    else:
        df[dt_column] = pd.to_datetime(df[dt_column])
        df['YearNum'] = df[dt_column].dt.year
        df['MonthNum'] = df[dt_column].dt.month
    #return the dataframe
    return df

#function to limit to a month range
def month_range(df, start, end):
    """
    filters the df by dropping months not in the range
    :param df: pandas dataframe
    :param start: start month of range to keep, number of month; int
    :param end: end month of data to keep, number of month int
    :return: dataframe with filtered months
    """
    df2 = df[df.MonthNum >= start]
    df2 = df2[df2.MonthNum <= end]
    return df2

#function to limit to a year range
def year_range(df, start, end):
    """
    filters the df by dropping years not in the range
    :param df: pandas dataframe
    :param start: start year of range to keep, number of year; int
    :param end: end year of data to keep, number of month int
    :return: dataframe with filtered years
    """
    df2 = df[df.YearNum >= start]
    df2 = df2[df2.YearNum <= end]
    return df2

#main function that will plot the data
def scatter_plot(df, dt_column='Date', startMonth=5, endMonth=9, startYear=2018, endYear=2021, x='Date', y='NDVI',
                 trendline=False, title='', x_title='Date', y_title='NDVI Value', polynomial=1):

    #add year and month columns and filter by the months and years
    df1 = add_year_and_month(df, dt_column)
    df2 = month_range(df1, startMonth, endMonth)
    df2 = year_range(df2, startYear, endYear)


    if trendline:
        # fix the issue with plotting the dates and a trendline
        df2.reset_index(inplace=True)
        df2[x_title] = df2[x_title].apply(mpl_dates.date2num)
        # drop the sensor and the polygon lable
        df2 = df2.drop(['sensor', 'region'], axis=1)
        df2 = df2.astype(float)
        # print(df2)

        # plot the data
        x_data = df2[x]
        y_data = df2[y]
        # make the scatter plot
        plt.scatter(x_data, y_data)
        # add the lables
        plt.title(title)
        plt.xlabel(x_title)
        plt.ylabel(y_title)
        z = np.polyfit(x_data, y_data, polynomial)
        p = np.poly1d(z)
        plt.plot(x_data, p(x_data), "r--")

    else:
        # plot the data
        x_data = df2[x]
        y_data = df2[y]
        # make the scatter plot
        plt.scatter(x_data, y_data)
        # add the lables
        plt.title(title)
        plt.xlabel(x_title)
        plt.ylabel(y_title)

    plt.show()


def yearly_summary_stats(df, dt_column='Date', startYear=2018, endYear=2021, startMonth=5, endMonth=9, value='NDVI', group_by='YearNum'):

    #add year and month columns and filter by the months and years
    df1 = add_year_and_month(df, dt_column)
    df2 = month_range(df1, startMonth, endMonth)
    df2 = year_range(df2, startYear, endYear)

    #get the summary stats for the NDVI values for each year
    return df2[[group_by, value]].groupby(group_by).describe()



#=======================================================================================================================
#                   1. Run the Functions
#=======================================================================================================================

"""
The data:

ls_roi_df 
ls_polys_df 
sl_roi_df
sl_polys_df 
"""

# sl_polys_df
# scatter_plot(sl_polys_df, title='Sentinel-2 BB Polygons 2018-2021', trendline=True)
# f = yearly_summary_stats(sl_polys_df)
# print(f)

# sl_roi_df
# scatter_plot(sl_roi_df, title='Sentinel-2 Surrounding Area 2018-2021', trendline=True)
# print(yearly_summary_stats(sl_roi_df))

# ls_polys_df
scatter_plot(ls_polys_df, title='Landsat BB Polygons 2008-2021', trendline=True, startYear=2008, polynomial=1)
# print(yearly_summary_stats(ls_polys_df, startYear=2018))

# ls_roi_df
# scatter_plot(ls_roi_df, title='Landsat Surrounding Area 2008-2021', trendline=False, startYear=2008)
# print(yearly_summary_stats(ls_roi_df, startYear=2008))

