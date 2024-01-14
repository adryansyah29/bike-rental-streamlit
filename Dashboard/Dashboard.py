import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

sewasepedajam_df=pd.read_csv("dashboard/all_data.csv")
sewasepedajam_df.head()