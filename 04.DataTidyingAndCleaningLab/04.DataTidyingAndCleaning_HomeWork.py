import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


from Utils.Functions.func_fix_column_names import snake_case
from Utils.Functions.func_convert_units_kg import units_to_kg
from Utils.Functions.func_spanish_to_english import translator
from Utils.Functions.func_parse_trimesters import parse_trimester
from Utils.Dicts.dict_graph_rating_colums import rating_columns
from Utils.Lists.stats_Raiting_Columns import statistical_columns
from Utils.Functions.func_helper_query_dataset import query_dataframe
from Utils.Functions.func_helper_normalize_text import normalize_text
from Utils.Dicts.dict_Country_on_Continent import country_to_continent
from Utils.Functions.func_helper_normalize_dates import normalize_dates
from Utils.Functions.func_helper_normalize_month import normalize_month

from Utils.Functions.func_fix_date_multiColumns import convert_date_multiColumns






indent = " " * 0
base_path = "F:/GitHub/DataScience"

# Loading dataset config CSV
config_path = os.path.join(base_path, "Utils", "Configs", "datasets_config.csv")
datasets_df = pd.read_csv(config_path)

# Convert CSV config into dictionary with full paths
dataset_paths = {
    row['name']: os.path.join(base_path, row['path'].lstrip("/").lstrip("\\"))
    for _, row in datasets_df.iterrows()
}

cofee_path = dataset_paths.get('coffee_data')
coffee_data = pd.read_csv(cofee_path, encoding='ISO-8859-1')



pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.precision', 2)
#coffee_data = pd.read_csv("lab/merged_data_cleaned.csv")

#query_dataframe(coffee_data, filepath=cofee_path, encoding='ISO-8859-1')

###################################################################
###################### 1 Reading Data #############################
###################################################################



print(f"{'':48}")
print(indent + "********* PROBLEM 1. READ THE DATASET **********")
print(indent + "********* Begin dataset observation ************")
print(f"{'':48}\n" * 1)
print(indent + f"DataFrame.dimensions: {coffee_data.shape}")
print(f"{'':48}")
print(indent + "DataFrame.coluns and rows:")
print(f"{'':48}")
print(coffee_data)
print(f"{'':48}")
print(coffee_data.columns)
print(f"{'':48}")
print(coffee_data.dtypes)
print(f"{'':48}\n" * 3)
print(indent + "DataFrame's Initial Columns:\n")
print(f"--------------------------------------")
print(f"--------------------------------------")
cols = list(coffee_data.columns)
for i in range(0, len(cols), 5):
    print(cols[i:i+5])
print(f"--------------------------------------")
print(f"{'':48}")
print(f"--------------------------------------")

print(indent + "\nData Types:\n", coffee_data.dtypes)
print(indent + f"--------------------------------------")
print(f"{'':48}")
print(indent + f"--------------------------------------")

print("\nFirst few rows:\n", coffee_data.head())
print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 1. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)


###################################################################
################# 2 DataSet observation ###########################
###################################################################
print(
    f"""    {indent} "********** PROBLEM 2. OBSERVATIONS AND FEATURES. ********* 
    {indent} "********** Observations are there? How many features? ********
    {indent} "********** Which features are numerical, and which are categorical? ******
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN DATASET OBSERVATION " + "*" * 9)
print(f"{'':48}\n" * 1)
print(indent + f"\nNumber of observations: {coffee_data.shape[0]}")
print(indent + f"Number of features: {coffee_data.shape[1]}")

numerical = list(coffee_data.select_dtypes(include=[np.number]).columns)
categorical = list(coffee_data.select_dtypes(include='object').columns)

if 'Unnamed: 0' in numerical:
    numerical.remove('Unnamed: 0')

print(f"{'':48}\n" * 1)
print(indent + f"\nNumber of Numerical features: {len(numerical)}")
print(indent + "\nNumerical features:")
for i in range(0, len(numerical), 5):
    print(numerical[i:i+5])

print(indent + f"\nNumber of Categorical features: {len(categorical)}")
print(indent + "\nCategorical features:")
for i in range(0, len(categorical), 5):
    print(categorical[i:i+5])

print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 2. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)


########################################################################
################# 3 Column manipulation ################################
########################################################################
print(
    f"""    {indent}********** PROBLEM 3. COLUMNS MANIPULATION. ********* 
    {indent}********** MAKE COLUMNS NAMES MORE PYTHONIC. ********
    {indent}********** CONVERT COLUMN NAMES TO SNAKE_CASE ******* 
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 1)
print(indent + "DataFrame. Initial Columns before renaming:\n")
coffee_data_columns_renamed = coffee_data.columns.map(snake_case)
coffee_data_columns_original_names = coffee_data.columns.copy()
coffee_data.columns = coffee_data_columns_renamed
print(coffee_data_columns_original_names)
print(f"{'':48}\n" * 1)
print("DataFrame. Columns after being renamed:\n")
print(coffee_data.columns)
coffee_data.set_index('unnamed: 0', inplace=True)
print(f"{'':48}\n" * 1)
#print(coffee_data.index.name)
print(indent + f"Index column for our DataFrame is: {coffee_data.index.name}")
print("DataFrame. Columns after declaring Index column:\n")
print(coffee_data.columns)
print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 3. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)


############################################################################
########################## 4 Bag Weight ####################################
############################################################################
print(
    f"""    {indent}********** PROBLEM 4. BAG WEIGHT. ********* 
    {indent}********** WHAT"S UP WITH BAG WEIGHT? ********
    {indent}********** MAKE ALL NECESSARY CHANGES TO THE COLUMN VALUES . ******* 
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 1)
print(coffee_data["bag_weight"])
print(f"{'':48}\n" * 1)
print("Initial values in [bag_weight] :\n")
print(coffee_data["bag_weight"].unique())

print(
    f"""
    {indent}[Bag.Weight] column contains as many different measurment units as you can possibly think of.
    Column should be normalized with a single unit, most likely kilogram as ubiversal SI unit for measuring weight.
    """
)

print(
    f"""
    {indent}First we are going to check if [Bag.Weight] column contains NaN as a values.
    """
)

print(coffee_data["bag_weight"].isna())
print(coffee_data["bag_weight"].isna().any())

coffee_data["is_missing"] = coffee_data["bag_weight"].isna()
print(coffee_data[["bag_weight", 'is_missing']])
print(coffee_data["bag_weight"].isna().sum())
print('------------------------------------------------')
# for value, missing in zip(coffee_data["Bag.Weight"], coffee_data["Bag.Weight"].isna()):
#     print(f"{value} -> Missing: {missing}")

print(
    f"""
    {indent}For our relief and best surprise [bag_weight] column does not have any NaN as a values.
    We can now convert all these different measurement units into a sigle one. THE ONE!!!
    """
)


print(
    f"""
    {indent}We are going to call a custom made function "units_to_kg" which are going to 
    convert all different units to a kilogram. Thus it we will be more convinient for us 
    if we need to use [bag_weight] for further calculation  
    """
)

coffee_data["bag_weight [kg]"] = coffee_data["bag_weight"].apply(units_to_kg)
print(coffee_data[["bag_weight", "bag_weight [kg]"]].head(10))
print(f"{'':48}\n" * 1)

print(
    f"""
    {indent}After applying "units_to_kg" to [bag_weight] now all values are in same unit - kilogram.
    """
)

print(coffee_data["bag_weight [kg]"].unique())

print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 4. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)


####################################################################
########## 5 Harvester of Sorrow. deal with it! YOU MUST ###########
####################################################################
print(
    f"""    {indent}********** PROBLEM 5. DATES.   ********* 
    {indent}********** SLIGHTLY NASTIER? SLIGHTLY???********
    {indent}********** FIX THE HARVEST YEAR< EXPIRATION DATE AND GRADING DATES. ******* 
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 2)

print(
    f"""
    {indent}Firts we will check the initial values in both [grading_date] and [expiration]
    columns and based on whats in it, we are going to do some magic  
    """
)

#### converting dates in ["grading_date", "expiration"] columns to something easier to work with -> %Y-%m-%d
print(coffee_data[["grading_date", "expiration"]])

print(
    f"""
    {indent}Both columns contains dates in format that only Chuck Noris can use for further calculation.   
    But we are weak. We need something like "%Y-%m-%d"
    """
)

print(
    f"""
    {indent}We are going to use another custom function - convert_date_multiColumns wich will convert 
    data in both [grading_date] and [expiration] columns to "%Y-%m-%d"
    """
)

coffee_data_expiration_dates = convert_date_multiColumns(coffee_data, ["grading_date", "expiration"])
print(coffee_data_expiration_dates[["grading_date", "expiration"]])
print(coffee_data_expiration_dates[["grading_date", "expiration"]].isna().any())


print(
    f"""
    {indent}Both [grading_date] and [expiration] are now with "%Y-%m-%d" as a date format. Looks like there are no any NaNs
    as a values in these columns. So we are good
    """
)
print(f"{'':48}\n" * 2)

print(
    f"""
    {indent}Moving on with [harvest_year] column.
    """
)
print("Harvest Year")
print(f"{'':48}")
print(coffee_data["harvest_year"].unique())

print(f"{'':48}\n" * 2)

print(
    f"""
    {indent} This column contains quite a lot different types of date formats. It also have spanish words init. 
    It appears that we have to deal with only years, month to month as a period, and some trimesters ->
    like "4T/20100" as a harvest period.
    """
)

print(f"{'':48}")

print(
    f"""
    {indent} We will start to clear all differences and inconsistencies one by one. For the beginning we can try 
    to translate all spanish words to English. For this purpose  we have custom dictionaty "dict_Es_to_En" 
    and a suctom function that will use this dictionary to translate what needs to be translated
    """
)

print(f"{'':48}")


print(
    f"""
    {indent} We will try to convert this trimesters dates into "%Ъ-%мп-%д" формат
    """
)

print(f"{'':48}")
coffee_data['harvest_year_original'] = coffee_data['harvest_year'].copy()

coffee_data['harvest_year_en'] = coffee_data['harvest_year'].apply(translator)
print(coffee_data['harvest_year_en'].unique())
print(f"{'':48}")
coffee_data['harvest_year'] = coffee_data['harvest_year_en']

coffee_data[["harvest_trimester_start", "harvest_trimester_end"]] = (
    coffee_data["harvest_year"]
    .apply(parse_trimester)
    .apply(pd.Series)
)
print(f"{'':48}")
print(coffee_data[["harvest_year", "harvest_trimester_start", "harvest_trimester_end"]]
      .dropna()
      .head(10))


coffee_data['harvest_normalized'] = coffee_data['harvest_year'].apply(normalize_dates)
print(f"{'':48}")
print(
    f"""
    {indent} Това са нормализираните дати като имана-дата-месец
    """
)
print(coffee_data['harvest_normalized'].dropna().unique())


print(f"{'':48}")
print(
    f"""
    {indent} ще се опитаме да премахнем описателния характер в датите като "january through april",
    новите дати трябва да са във формат "January - April"
    """
)

coffee_data['harvest_year_norm'] = coffee_data['harvest_year'].apply(normalize_month)
print(coffee_data['harvest_year_norm'].unique())

print(f"{'':48}")

print(
    coffee_data[
        ["harvest_year",  "harvest_trimester_start", "harvest_trimester_end"]
    ]
    .dropna(subset=["harvest_trimester_start"])
    .head(10)
)


print(f"{'':48}")
print(
    f"""
    {indent} Резултатът го запазваме в dataset-a Който ще продължим да обработваме по нататък
    """
)

coffee_data["harvest_year_clean"] = (coffee_data["harvest_year"].apply(translator).apply(normalize_month))
coffee_data[["harvest_trimester_start", "harvest_trimester_end"]] = (coffee_data["harvest_year_clean"].apply(parse_trimester).apply(pd.Series))
print(coffee_data.columns)

coffee_data = coffee_data.rename(columns={
    "harvest_trimester_start": "harvest_time_start",
    "harvest_trimester_end": "harvest_time_end"
})
print(f"{'':48}")
print(coffee_data.columns)
print(f"{'':48}\n" * 2)
print(
    f"""
    {indent} Добавихме две нови колони които държат датата на стартиране на беритбата и датата на край на беритбата
    на кафето, като са трансформирани тримесечните периоди  
    """
)
print(coffee_data[["harvest_year", "harvest_time_start", "harvest_time_end"]].dropna().head(10))

print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 5. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)


####################################################################
###################### Problem 6  CONTRIES #########################
####################################################################

print(
    f"""    {indent}********** PROBLEM 6. ЦОНТРИЕС.   ********* 
    {indent}********** HOW MANY COFFEES ARE THERE WITH UNKNOWN COUNTRIES OF ORIGIN? ********
    {indent}********** WHAT CAN YOU DO ABOUT THEM?. ******* 
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 2)

print(
    f"""
    {indent}Ще се опитаме да нормализираме данните до малки букви и да премахем всякакви интервали в началото и края
    """
)

countries = coffee_data['country_of_origin'].astype(str).str.strip().str.lower()
print(countries)

print(f"{'':48}\n" * 2)

print(
    f"""
    {indent}Слагаме си маркери като за какво считамне за 'unknown'
    """
)

unknown_markers = ['', 'unknown', 'n/a', 'unk', 'none']
unknown_countries = countries.isin(unknown_markers) | coffee_data['country_of_origin'].isna()

totalUnknownCount = unknown_countries.sum()
print(f"Number of coffee with unknown countries of origin is: {totalUnknownCount}")

print(f"{'':48}")

print(
    f"""
    {indent}Според това което получихме има само едно кафе с 'unknown' country_of_origin
    """
)
print(coffee_data[unknown_countries][['region', 'producer', 'mill']].head(10))
print("---------finding more info for nan's")
unknown_rows = coffee_data[unknown_countries]
print(unknown_rows[['region', 'producer', 'mill', 'farm_name', 'company']].head(15))
print("here we go")
print(coffee_data.loc[1197])

print(
    f"""
    {indent}According to information that we have gather, we can еither drop tjat line, or we can try to populate 
    'country_of_origin' based on the information for 'racafe & cia s.c.a' country of production.  
    Printing everythong for index 1197 to find some meaningful information. We can find some info in owner and  
    owner_1 columns we can see 'Racafe & Cia S.C.A'.
    According to Internet https://drwakefield.com/producer/racafe/ is Columbian coffee brand
    """
)

print(
    f"""
    {indent}We can either Insert Columbia as a 'country_of_origin' if we are sure about that. 
    Or we can just leave it as it is.
    
    """
)

print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 6. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)


####################################################################
###################### Problem 7  OWNERS ###########################
####################################################################

print(
    f"""    {indent}********** PROBLEM 7. OWNERS.   ********* 
    {indent}********** THERE ARE TWO SUSPICIOUS COLUMNS, NAMED 'OWNER', AND 'OWNER_1'? ********
    {indent}********** WHAT CAN YOU DO ABOUT THEM?. ******* 
    {indent}********** IS THERE ANY LINK TO 'PRODUCER'?. *******
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 2)

print(
    f"""
    {indent}Нека първо сравним двете колони, какво има в тях като данни, има ли някакви видими разлики?

    """
)
print(f"{'':48}")
owners_column_diff = coffee_data[['country_of_origin', 'region', 'producer', 'aroma', 'flavor', 'owner', 'owner_1']]
diff_owners = owners_column_diff[owners_column_diff['owner'] != owners_column_diff['owner_1']]
print(f"{'':48}")
print("column comparison of 'owner' and 'owner_1' differ:\n")
print(diff_owners.head(15))
print(f"{'':48}")
same_owners = (coffee_data['owner'] == coffee_data['owner_1']).all()
print(f"all 'owner' and 'owner_1' always equal? {same_owners}")
print(f"{'':48}")
count_diff = (coffee_data['owner'] != coffee_data['owner_1']).sum()
print(f"Total number of different records in 'owner' and 'owner_1' are {count_diff} ")
print(f"{'':48}")
print(
    f"""
    {indent}На пръв поглед разликата в колоните изглежда да е като само големи/малки букви?
    Записите и в двете колони изглеждат идентични
    """
)


print(f"{'':48}")
print(
    f"""
    {indent}Ще проверим дали хипотезата ни е вярна и наистина разликите са само Case sensitive
    """
)

normalize_differences = (
    coffee_data['owner'].str.strip().str.lower() != coffee_data['owner_1'].str.strip().str.lower()
)

total_count_case_insesitive = normalize_differences
print(f"Case insensitive difference is: {total_count_case_insesitive}")
print(f"{'':48}")

print(
    f"""
    {indent}Хипотезата изглежда се потвърди и е вярна. Разликите са само в големите и малки букви с които са 
    изписани стойностите в двете колони
    """
)

print(
    f"""
    {indent}На база на това можем да дропнем 'owner_1' колоната като тя не ни носи никаква допълнителна информация
    """
)


mismatched_normalized = coffee_data[normalize_differences][
    ['country_of_origin', 'region', 'producer', 'owner', 'owner_1']
]

print(mismatched_normalized.head(10))

owner_1_dropped = coffee_data.drop(columns=['owner_1'], inplace=True)
owner = list(coffee_data.select_dtypes(include='object').columns)


print(f"{'':48}\n" * 1)
for i in range(0, len(owner), 5):
    print(owner[i:i+5])


print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 7. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)


####################################################################
############## Problem 8  COLORS BY COUNTRY ########################
####################################################################

print(
    f"""    {indent}********** PROBLEM 8. COFFEE COLOR BY COUNTRY AND CONTINENT.   ********* 
    {indent}********** CREATE A TABLE TO SHOW HOW MANY COFFEE OF EACH COLOR PER COUNTRY ********
    {indent}********** LEAVE THE MISSING VALUES AS THEY ARE. ******* 
    {indent}********** DO THE SAME FOR CONTINETS. *******
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 2)


print(f"{'':48}")
print(
    f"""
    {indent}Table bellow shoes the number of coffee per colors per country 
    """
)


country_color_table = (
    coffee_data.groupby(['country_of_origin', 'color'])
    .size()
    .reset_index(name='coffee_count')
    .sort_values(by=['country_of_origin', 'coffee_count'], ascending=[True, False])
)
print(country_color_table)


print(f"{'':48}")
print(
    f"""
    {indent}for the continent tables we have created dictionary -> 'dict_Country_on_Continent' which 
    maps coffee distributor country to its continent
    """
)

coffee_data['continent'] = coffee_data['country_of_origin'].map(country_to_continent)

print(f"{'':48}")
print(
    f"""
    {indent}Table bellow shoes the number of coffee per colors per continents 
    """
)

continent_color_table = (
    coffee_data.groupby(['continent', 'color'])
    .size()
    .reset_index(name='coffee_count')
    .sort_values(by=['continent','coffee_count'], ascending=[True, False])
)
print(continent_color_table)

print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 8. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)

############################################################################
######################### Problem 9  RATINGS ###############################
############################################################################

print(
    f"""    {indent}********** PROBLEM 9. RATINGS.   ********* 
    {indent}********** THE COLUMNS FROM 'AROMA' UP TO 'MOISTURE' REPRESENT SUBJECTIVE RATINGS ********
    {indent}********** SHOW THE MEANS AND RANGE. DRAW HISTOGRAM AND/OR BOXPLOTS AS NEEDED ******* 
    {indent}********** TRY CORRELATIONS WHAT IS UP WITH ALL THOSE RATINGS. *******
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 2)

print(coffee_data[rating_columns].dtypes)
print(f"{'':48}")

for col in rating_columns:
    valid_data = coffee_data_expiration_dates[col].dropna().iloc[0] if not coffee_data[col].dropna().empty else None

print(f"{col}: {valid_data}")

print(f"{'':48}")

print(coffee_data[rating_columns].describe())

print(f"{'':48}")
print(
    f"""
    {indent}В таблицата долу са показани минималните и максималните стойности на всяка от изброените колони

    """
)
for col in rating_columns:
    print(f"{col}: min={coffee_data[col].min()}, max={coffee_data[col].max()}")

print(f"{'':48}")

#### Mean, Min, Max, Range

# stat_desc = coffee_data[statistical_columns].describe().T
# stat_desc['range'] = stat_desc['max'] - stat_desc['min']
# print(stat_desc[['mean', 'min', 'max', 'range']])
#
# for column in statistical_columns:
#     plt.figsize = (14, 8)
#     plt.hist(coffee_data[column].dropna(), bins=20, color='skyblue', edgecolor='black')
#     plt.suptitle("Coffee Quality Ratings Distribution")
#     plt.xlabel('Rating')
#     plt.ylabel('Frequency')
#     plt.grid(True)
#     plt.tight_layout()
#     plt.subplots_adjust()
#     plt.show()


score_counts = coffee_data['aroma'].dropna().round(1).value_counts().sort_index()

plt.figure(figsize=(10, 5))
score_counts.plot(kind='bar', color='skyblue')
plt.title("Frequency of Aroma Scores")
plt.xlabel("Aroma Score")
plt.ylabel("Number of Coffees")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# Set up subplot grid: 3 rows x 4 columns
fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(15, 7))
axes = axes.flatten()  # Flatten to iterate easily

# Loop through each column and plot histogram
for i, col in enumerate(rating_columns):
    axes[i].hist(coffee_data[col].dropna(), bins=20, color='skyblue', edgecolor='black')
    axes[i].set_title(f"{col.capitalize()} Distribution")
    axes[i].set_xlabel(col, labelpad=10)
    axes[i].set_ylabel("Frequency")
    axes[i].grid(True)

# Remove any unused subplots if columns < 12
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()


correlation_matrix = coffee_data[statistical_columns].corr()
print(correlation_matrix)


plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=1, vmax=1, fmt=".2f")
plt.title("Correlation Between COfee Quality Ratings")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()


ratings_clean = coffee_data[statistical_columns].dropna()

# Set up the plot
plt.figure(figsize=(14, 8))
sns.boxplot(data=ratings_clean, orient='h', palette='Set2')
plt.title('Boxplots of Coffee Rating Features')
plt.xlabel('Score')
plt.ylabel('Feature')
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


ratings_clean = coffee_data[statistical_columns].dropna()

# Melt the DataFrame for seaborn
melted = ratings_clean.melt(var_name='Feature', value_name='Score')

# Plot
plt.figure(figsize=(14, 6))
sns.boxplot(x='Feature', y='Score', data=melted, palette='Set2')
plt.title('Boxplots of Coffee Rating Features')
plt.xticks(rotation=45)
plt.xlabel('Feature')
plt.ylabel('Score')
plt.ylim(5, 90)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


scaled_data = coffee_data[statistical_columns].copy()

# Apply MinMax scaling to 0–10 range
scaler = MinMaxScaler(feature_range=(0, 10))
scaled_data[rating_columns] = scaler.fit_transform(scaled_data[rating_columns])

# Melt for seaborn
melted_scaled = scaled_data.melt(var_name='Feature', value_name='Score')

# Plot boxplot
plt.figure(figsize=(14, 6))
sns.boxplot(x='Feature', y='Score', data=melted_scaled, palette='Set3')
plt.title('Boxplots of Coffee Ratings (Normalized)')
plt.xticks(rotation=45)
plt.ylabel('Normalized Score (0–10)')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print(f"{'':48}")
print(
    f"""
    {indent}От няколкото ртазлични графики моцем да направим някои важни за нашия анализ изводи.
    От корелационната карта виждаме, че има доста висока зависимост (0.9) между вида кафе и послевкуса-а
    флажоур <-> афтертасте.
    Виждаме и висока корелация между вкус и крайна оценка flavour <-> total_cup_points (0.85)
    """
)

print(
    f"""
    {indent}Наблюдават се и по-слаби корелации. Например sweetnes <-> flavour (0.29), moisture <-> aroma (-0.13),
    moisture <-> total_cup_points (-0.12). Можем да кажем, че тези показатели имат ограничено влияние върху общата оценка
    """
)

print(
    f"""
    {indent}От boxplots графиката виждаме, че няколко показателя имат по-широки кутийки и ясно видими отклонения, 
    (Аромат, Вкус, Послевкус, Киселинност, Плътност и Баланс:). Техните медиани са около 8.5 - 9.0 което подсказва за 
    високи оценки по тези характеристики.
    """
)

print(
    f"""
    {indent}От boxplots графиката също така се виждат и някои характеристики с много ниска променливост. 
    Техните стойности са почти еднакви или са изключително близки една до друга (clean_cup, sweetnes )
    
    """
)

print(f"{'':48}")
print(indent + "*" * 9 + " END OF QUERYING PROBLEM 9. " + "*" * 9)
print(indent + f"{'':48}\n" * 2)

####################################################################
######### Problem 10  HIGH-LEVEL ERRORS ############################
####################################################################

print(
    f"""    {indent}********** PROBLEM 10. HIGH-LEVEL ERRORS.   ********* 
    {indent}********** CHECK THE COUNTRIES AGAINST THE REGION NAMES, ALTITUDES AND COMPANIES. ********
    {indent}********** ARE THERE ANY DISCREPANCIES? ******* 
    {indent}********** TAKE A LOOK AT ALTITUDES..... *******
    """
)
print(f"{'':48}")
print(indent + "*" * 9 + " BEGIN COLUMN MANIPULATION " + "*" * 9)
print(f"{'':48}\n" * 2)


#print(coffee_data['region'].unique())


print(
    f"""
    {indent}Проверяваме страна срещу регион
    """
)
country_region = coffee_data.groupby('country_of_origin')['region'].unique()
for country, regions in country_region.items():
    print(f"{country}: {regions}")


print(
    f"""
    {indent}Доста грешки в изписването и с асайнването на регионите към дадена държава.
    например имаме 'United States' с регион 'antioquia'. Antioquia е в Colombia
    Имаме - Colombia с регион '52 narino (exact location: mattituy; municipal region: florida code 381'
    което изглежда като грешно, недописано  и т.н.
    Имаме и 'dummy' стойности -> Brazil с регион ['ммм', 'тест']
    и още много . ..
    """
)


country_region_map = {
    'Brazil': ['test', 'nan', 'cerrado', 'sul de minas - carmo de minas', 'grama valley'],
    'United States': ['antioquia', 'berastagi', 'central america', 'chikmagalur'],

}


coffee_data['region'] = coffee_data['region'].apply(normalize_text)
bad_regions = ['nan', 'test', 'mmm', 'na', 'none']

coffee_data = coffee_data[~coffee_data['region'].isin(bad_regions)]



print(f"{'':48}\n" * 2)
#### check altitudes

altitude_check = coffee_data[
    (coffee_data['altitude_mean_meters'] < coffee_data['altitude_low_meters']) |
    (coffee_data['altitude_mean_meters'] > coffee_data['altitude_high_meters'])
]
print(f"{'':48}")
print(
    f"""
    {indent}Rows where mean is outside low-high range:
    """
)


print(altitude_check[['country_of_origin', 'region', 'altitude_low_meters', 'altitude_high_meters', 'altitude_mean_meters']])

print(f"{'':48}")

#### this prints:
'''''
Rows where mean is outside low-high range:
Empty DataFrame
Columns: [country_of_origin, region, altitude_low_meters, altitude_high_meters, altitude_mean_meters]
Index: []
'''''

#### which implies that the altitude cleaning and normalization appears to be correct.
#### no obvious discrepancies (like a mean outside the min/max range) were found.
#### the data seems internally consistent for altitudes.

print(coffee_data[['altitude_low_meters', 'altitude_high_meters', 'altitude_mean_meters']].isnull().sum())

same_altitude = coffee_data[
    (coffee_data['altitude_low_meters'] == coffee_data['altitude_high_meters']) &
    (coffee_data['altitude_low_meters'] == coffee_data['altitude_mean_meters'])
]
print(f"{'':48}")
print(f"Rows with all altitude values equal: {len(same_altitude)}")
print(same_altitude[['country_of_origin', 'region', 'altitude_low_meters']].value_counts().head(10))

print(f"{'':48}")

# Step 1: Create the 'altitude_all_equal' column
coffee_data['altitude_all_equal'] = (
    (coffee_data['altitude_low_meters'] == coffee_data['altitude_high_meters']) &
    (coffee_data['altitude_low_meters'] == coffee_data['altitude_mean_meters'])
)

print(f"{'':48}")
implausible_altitudes = coffee_data[
    (coffee_data['altitude_all_equal']) & (coffee_data['altitude_mean_meters'] < 100)
]

print(f"{'':48}")
print(implausible_altitudes[['country_of_origin', 'region', 'altitude_mean_meters']])


#### there are some not realistic altitudes for South America  mountain countries