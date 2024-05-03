import streamlit as st
import pandas as pd
import numpy as np

# Function to perform calculations on the data
def get_stats(data,location):
    
    colnames=data.columns
    location_col=colnames[0]
    job_title_col=colnames[1]
    hourly_rate_col=colnames[2]
    tenure_col=colnames[3]


    data=data.loc[~data[hourly_rate_col].isna(),:]
    data=data.loc[~data[job_title_col].isna(),:]

    jobs=list(set(data[job_title_col]))

    data[hourly_rate_col]=data[hourly_rate_col].astype(float)

    stats=pd.DataFrame(columns=["Job_Title","Yrs_Peer_Min","Yrs_Peer_Max","Yrs_Peer","Yrs_Location","Min","10_percentile","25_percentile","33_percentile","Median","66_percentile","75_percentile","90_percentile","Max","Mean","N_Total","N_Peer","Location_Mean","Location_N"])

    for job in jobs:
        temp_data=data.loc[data[job_title_col]==job,:]
        non_target_location_data=data.loc[((data[job_title_col]==job) & (data[location_col]!=location)),:]
        target_location_data=data.loc[((data[job_title_col]==job) & (data[location_col]==location)),:]
        
        location_mean=np.nanmean(target_location_data.loc[target_location_data[location_col]==location,hourly_rate_col])
        location_n=len(target_location_data.loc[target_location_data[location_col]==location,hourly_rate_col].index)

        try:
            yrs_peer_min=np.nanmin(non_target_location_data.loc[non_target_location_data[location_col]!=location,tenure_col])
        except ValueError:
            yrs_peer_min=np.NaN

        try:    
            yrs_peer=np.nanmean(non_target_location_data.loc[non_target_location_data[location_col]!=location,tenure_col])
        except ValueError:
            yrs_peer=np.NaN

        try:
            yrs_peer_max=np.nanmax(non_target_location_data.loc[non_target_location_data[location_col]!=location,tenure_col])
        except ValueError:
            yrs_peer_max=np.NaN

        try:
            yrs_location=np.nanmean(target_location_data.loc[target_location_data[location_col]==location,tenure_col])
        except ValueError:
            yrs_location=np.NaN


        minimum=round(np.nanmin(temp_data[hourly_rate_col]),2)
        percent10=round(np.nanpercentile(temp_data[hourly_rate_col],10),2)
        percent25=round(np.nanpercentile(temp_data[hourly_rate_col],25),2)
        percent33=round(np.nanpercentile(temp_data[hourly_rate_col],33.33),2)
        percent50=round(np.nanpercentile(temp_data[hourly_rate_col],50),2)
        percent66=round(np.nanpercentile(temp_data[hourly_rate_col],66.66),2)
        percent75=round(np.nanpercentile(temp_data[hourly_rate_col],75),2)
        percent90=round(np.nanpercentile(temp_data[hourly_rate_col],90),2)
        maximum=round(np.nanmax(temp_data[hourly_rate_col]),2)
        mean=round(np.nanmean(temp_data[hourly_rate_col]),2)
        n_total=len(temp_data.index)
        n_peer=len(non_target_location_data.index)

        # stats.loc[len(stats.index)] = [job,job_dept_dict[job],yrs_peer_min,yrs_peer_max,yrs_peer,yrs_location,minimum,percent10,percent25,percent50,percent75,percent90,maximum,mean,n_total,n_peer,location_mean,location_n]
        stats.loc[len(stats.index)] = [job,yrs_peer_min,yrs_peer_max,yrs_peer,yrs_location,minimum,percent10,percent25,percent33,percent50,percent66,percent75,percent90,maximum,mean,n_total,n_peer,location_mean,location_n]

    stats["Mean_Difference"]=stats["Location_Mean"]-stats["Mean"]
    stats["Mean_Difference"]=round(stats["Mean_Difference"],2)

    stats = stats.sort_values(['Job_Title'], ascending=(True))

    compa_ratio=stats[['Job_Title','Location_Mean','Mean_Difference','Min', '10_percentile', '25_percentile', '33_percentile','Mean','Median','66_percentile', '75_percentile',
        '90_percentile', 'Max','N_Total', 'N_Peer', 'Location_N','Yrs_Location','Yrs_Peer_Min', 'Yrs_Peer','Yrs_Peer_Max']]

    compa_ratio = compa_ratio.sort_values(['Job_Title'], ascending=(True))

    compa_ratio["Yrs_Location"]=round(compa_ratio["Yrs_Location"],2)
    compa_ratio["Yrs_Peer"]=round(compa_ratio["Yrs_Peer"],2)
    compa_ratio["Location_Mean"]=round(compa_ratio["Location_Mean"],2)
    compa_ratio["Mean"]=round(compa_ratio["Mean"],2)
    compa_ratio["Yrs_Location"]=round(compa_ratio["Yrs_Location"],2)
    compa_ratio["Median"]=round(compa_ratio["Median"],2)

    compa_ratio["Min_Compa"]=round(((compa_ratio["Location_Mean"]/compa_ratio["Min"])*100),2)
    compa_ratio["Mean_Compa"]=round(((compa_ratio["Location_Mean"]/compa_ratio["Mean"])*100),2) 
    compa_ratio["Median_Compa"]=round(((compa_ratio["Location_Mean"]/compa_ratio["Median"])*100),2) 
    compa_ratio["Max_Compa"]=round(((compa_ratio["Location_Mean"]/compa_ratio["Max"])*100),2)

    compa_ratio["Position_in_Range"]=round(((compa_ratio["Location_Mean"]-compa_ratio["Min"])/(compa_ratio["Max"]-compa_ratio["Min"]))*100,2)

    compa_ratio.columns=['Job Title', '{} Mean'.format(location), 'Mean Difference', 'Min', '10 percentile',
        '25 percentile', '33 percentile', 'Mean', 'Median', '66 percentile',
        '75 percentile', '90 percentile', 'Max', 'N Total', 'N Peer',
        '{} N'.format(location), 'Yrs {}'.format(location), 'Yrs Peer Min', 'Yrs Peer',
        'Yrs Peer Max', 'Min Compa', 'Mean Compa', 'Median Compa', 'Max Compa',
            'Position in Range']

    return(compa_ratio)

# Main function
def main():
    st.title("Compensation Statistics")

    st.header("Instructions")

    with st.expander("Input Data Type"):
        st.write("- Please upload your input data as a .csv file (in Excel, 'File' > 'Save As' > save as a csv)")
        st.write("- If there is no data (e.g. no tenure data for a position, etc), please leave the cell blank")
        st.write("- Please remove all dollar signs, `$`")
        st.write("- It probably won't be an issue, but weird spacing in the cells could mess things up")

    with st.expander("Column Names (column order matters, column names do not)"):
        st.write("- *First column*: names of the comparison locations/organizations")
        st.write("- *Second column*: job titles")
        st.write("- *Third column*: hourly rate")
        st.write("- *Fourth column*: tenure at the organization")
    
    with st.expander("Example Input Data"):
        test_data=pd.read_csv("ketchum_4_19_freshall.csv", index_col=None)
        st.write(test_data.iloc[:10,:])

    st.header("Name")
    location_name = st.text_input("Enter the name of the target city / organization exactly as it appears in the input data file")

    st.header("Input Data")
    uploaded_file = st.file_uploader("Upload Compensation Input Data", type=['csv'])
    
    st.header("Run Analysis")
    if st.button("Run Analysis") and uploaded_file is not None:
        uploaded_df=pd.read_csv(uploaded_file)

        location_stats=get_stats(uploaded_df,location_name)

        st.header("Results")
        st.download_button(
            label="Download Results",
            data=location_stats.to_csv(index=False),
            file_name='{}_final_stats.csv'.format(location_name),
            mime='text/csv'
        )
 
# Run the app
if __name__ == "__main__":
    main()
