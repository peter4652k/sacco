import streamlit as st
import pandas as pd
import os
from datetime import datetime


# =====================================================
# CONFIGURATION
# =====================================================

MEMBER_FILE = "members.csv"
LOAN_FILE = "loans.csv"


# =====================================================
# CREATE CSV DATABASES
# =====================================================

def create_files():

    if not os.path.exists(MEMBER_FILE):

        members = pd.DataFrame(columns=[
            "MEMBER ID",
            "NAME",
            "PHONE",
            "SAVINGS",
            "DATE REGISTERED"
        ])

        members.to_csv(MEMBER_FILE, index=False)


    if not os.path.exists(LOAN_FILE):

        loans = pd.DataFrame(columns=[
            "LOAN ID",
            "MEMBER ID",
            "MEMBER NAME",
            "LOAN AMOUNT",
            "INTEREST RATE",
            "INTEREST AMOUNT",
            "TOTAL PAYABLE",
            "DATE"
        ])

        loans.to_csv(LOAN_FILE, index=False)



create_files()



# =====================================================
# LOAD DATA
# =====================================================

def load_members():

    return pd.read_csv(MEMBER_FILE)



def load_loans():

    return pd.read_csv(LOAN_FILE)



# =====================================================
# SAVE DATA
# =====================================================

def save_members(data):

    data.to_csv(
        MEMBER_FILE,
        index=False
    )



def save_loans(data):

    data.to_csv(
        LOAN_FILE,
        index=False
    )



# =====================================================
# GENERATE MEMBER ID
# =====================================================

def generate_member_id():

    df = load_members()

    if len(df)==0:

        return "M001"

    else:

        number = len(df)+1

        return f"M{number:03}"



# =====================================================
# STREAMLIT DESIGN
# =====================================================


st.set_page_config(
    page_title="SACCO Management System",
    layout="wide"
)



st.title("🏦 SACCO MANAGEMENT SYSTEM")


menu = st.sidebar.selectbox(

    "MENU",

    [
        "Dashboard",
        "Register Member",
        "Search Member",
        "All Members"
    ]

)



# =====================================================
# DASHBOARD
# =====================================================


if menu=="Dashboard":

    st.header("SACCO Dashboard")


    members = load_members()


    total_members = len(members)


    if total_members > 0:

        total_savings = members["SAVINGS"].sum()

        average = members["SAVINGS"].mean()


    else:

        total_savings = 0

        average = 0



    col1,col2,col3 = st.columns(3)



    with col1:

        st.metric(
            "TOTAL MEMBERS",
            total_members
        )


    with col2:

        st.metric(
            "TOTAL SAVINGS",
            f"UGX {total_savings:,.0f}"
        )


    with col3:

        st.metric(
            "AVERAGE SAVINGS",
            f"UGX {average:,.0f}"
        )




# =====================================================
# REGISTER MEMBER
# =====================================================


elif menu=="Register Member":


    st.header("Register New Member")


    name = st.text_input(
        "Member Name"
    )


    phone = st.text_input(
        "Phone Number"
    )


    savings = st.number_input(
        "Initial Savings",
        min_value=0.0
    )



    if st.button("SAVE MEMBER"):


        members = load_members()



        if name=="":

            st.error(
                "Please enter member name"
            )


        else:


            member_id = generate_member_id()



            new_member = pd.DataFrame([{


                "MEMBER ID":member_id,

                "NAME":name,

                "PHONE":phone,

                "SAVINGS":savings,

                "DATE REGISTERED":
                datetime.now().strftime("%Y-%m-%d")


            }])



            members = pd.concat(
                [
                    members,
                    new_member
                ],
                ignore_index=True
            )



            save_members(
                members
            )



            st.success(
                f"Member {member_id} registered successfully"
            )




# =====================================================
# SEARCH MEMBER
# =====================================================


elif menu=="Search Member":


    st.header("Search Member")


    search = st.text_input(
        "Enter Member ID or Name"
    )



    if st.button("SEARCH"):


        members = load_members()



        result = members[

            (members["MEMBER ID"]
             .astype(str)
             .str.lower()
             ==
             search.lower())

            |

            (members["NAME"]
             .astype(str)
             .str.lower()
             ==
             search.lower())

        ]



        if len(result)==0:


            st.warning(
                "Member not found"
            )


        else:


            st.subheader(
                "Member Details"
            )


            st.dataframe(
                result,
                use_container_width=True
            )




# =====================================================
# ALL MEMBERS
# =====================================================


elif menu=="All Members":


    st.header(
        "Registered Members"
    )


    members = load_members()


    st.dataframe(
        members,
        use_container_width=True
    )
    # =====================================================
# LOAN FUNCTIONS
# =====================================================


def generate_loan_id():

    loans = load_loans()

    if len(loans) == 0:

        return "L001"

    else:

        number = len(loans) + 1

        return f"L{number:03}"



# =====================================================
# ADD LOAN MENU
# =====================================================


# Add this option inside the sidebar menu list in Part 1:

# "Add Loan",
# "Loan Dashboard"


# =====================================================
# ADD LOAN
# =====================================================


   elif menu == "Add Loan":


    st.header("Add Member Loan")


    members = load_members()



    if len(members)==0:

        st.warning(
            "No members registered yet"
        )

    else:


        member_name = st.selectbox(

            "Select Member",

            members["NAME"]

        )



        amount = st.number_input(

            "Loan Amount",

            min_value=0.0

        )


        interest_rate = st.number_input(

            "Interest Rate (%)",

            min_value=0.0,

            value=10.0

        )



        if st.button("SAVE LOAN"):


            member = members[

                members["NAME"] == member_name

            ].iloc[0]



            interest_amount = (

                amount *

                interest_rate /

                100

            )



            total_payable = (

                amount +

                interest_amount

            )



            loans = load_loans()



            loan_id = generate_loan_id()



            new_loan = pd.DataFrame([{

                "LOAN ID":
                loan_id,


                "MEMBER ID":
                member["MEMBER ID"],


                "MEMBER NAME":
                member["NAME"],


                "LOAN AMOUNT":
                amount,


                "INTEREST RATE":
                interest_rate,


                "INTEREST AMOUNT":
                interest_amount,


                "TOTAL PAYABLE":
                total_payable,


                "DATE":
                datetime.now()
                .strftime("%Y-%m-%d")


            }])



            loans = pd.concat(

                [

                    loans,

                    new_loan

                ],

                ignore_index=True

            )



            save_loans(loans)



            st.success(

                f"""
                Loan Approved

                Loan Amount:
                UGX {amount:,.0f}

                Interest:
                UGX {interest_amount:,.0f}

                Total Payable:
                UGX {total_payable:,.0f}
                """

            )





# =====================================================
# LOAN DASHBOARD
# =====================================================


elif menu == "Loan Dashboard":


    st.header(
        "Loan Dashboard"
    )


    loans = load_loans()



    if len(loans)==0:


        st.info(
            "No loans recorded"
        )


    else:


        total_loans = loans[
            "LOAN AMOUNT"
        ].sum()



        total_interest = loans[
            "INTEREST AMOUNT"
        ].sum()



        total_payable = loans[
            "TOTAL PAYABLE"
        ].sum()



        col1,col2,col3 = st.columns(3)



        with col1:

            st.metric(

                "TOTAL LOANS GIVEN",

                f"UGX {total_loans:,.0f}"

            )



        with col2:

            st.metric(

                "TOTAL INTEREST",

                f"UGX {total_interest:,.0f}"

            )



        with col3:

            st.metric(

                "TOTAL EXPECTED PAYMENT",

                f"UGX {total_payable:,.0f}"

            )



        st.subheader(
            "Loan Records"
        )


        st.dataframe(

            loans,

            use_container_width=True

        )





# =====================================================
# UPDATE SEARCH MEMBER SECTION
# =====================================================

# Replace the Search Member section from Part 1
# with this improved version


elif menu=="Search Member":


    st.header(
        "Search Member"
    )


    search = st.text_input(
        "Enter Member ID or Name"
    )


    if st.button("SEARCH"):


        members = load_members()


        loans = load_loans()



        result = members[

            (

            members["MEMBER ID"]
            .astype(str)
            .str.lower()
            ==
            search.lower()

            )

            |

            (

            members["NAME"]
            .astype(str)
            .str.lower()
            ==
            search.lower()

            )

        ]



        if len(result)==0:


            st.error(
                "Member not found"
            )


        else:


            member = result.iloc[0]


            st.subheader(
                "Member Information"
            )


            st.write(
                "Member ID:",
                member["MEMBER ID"]
            )


            st.write(
                "Name:",
                member["NAME"]
            )


            st.write(
                "Savings:",
                f"UGX {member['SAVINGS']:,.0f}"
            )



            member_loans = loans[

                loans["MEMBER ID"]

                ==

                member["MEMBER ID"]

            ]



            st.subheader(
                "Loan History"
            )



            if len(member_loans)>0:


                st.dataframe(

                    member_loans,

                    use_container_width=True

                )


            else:


                st.info(
                    "No loans found"
                )
