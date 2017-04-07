import pandas as pd

df_og = pd.read_csv("timesData_og.csv")

# STEP 0:
# ==============================================================================
# save just the last year
df = df_og[df_og.year == 2016]

# STEP 1:
# ==============================================================================
# convert number of students to proper type (ints, not strings with commas)
df['num_students'] = df['num_students'].apply(lambda x: str(x).replace(",", ""))

# note: it's okay to keep numerical values as strings, converted in graphing process


# STEP 2:
# ==============================================================================
# convert female:male ratio colon format into percent
def ratio_func(ratio):
    # for each "XX : XX" value...
    try:
        items = str(ratio).split(" : ")
        return int(items[0])/int(items[1]) * 100
    except ZeroDivisionError:
        # if 100% of females...
        return 100
    except ValueError:
        pass

df['female_male_ratio'] = df['female_male_ratio'].apply(ratio_func)

# STEP 3:
# ==============================================================================
# remove "%" from international students percentage column
df['international_students'] = df['international_students'].apply(lambda x: str(x).strip("%"))

# STEP 4:
# ==============================================================================
# clean up university ranking names: (1) delete entries with range of rank given
# (keep top 200 only), and (2) remove "=" before some numbers

# filter out ranges
df = df[df.world_rank.str.contains("-") == False]

# delete "=" character
df['world_rank'] = df['world_rank'].apply(lambda x: str(x).replace("=", ""))

# STEP 5:
# ==============================================================================
# remove unneeded columns:
del df['year']
del df['country']

# STEP 6:
# ==============================================================================
# replace NaNs with respective column median:

# first, replace messy symbols with NaNs
df.replace(to_replace = "-", value = float('nan'), inplace = True)
df.replace(to_replace = "nan", value = float('nan'), inplace = True)

# and now replace all NaNs with column median
for col in df.columns:
    if col == 'university_name':
        continue

    # otherwise perform for all columns
    df[col].fillna(df[col].median(), inplace = True)

# STEP 7:
# ==============================================================================
# and output to csv:
df.to_csv("timesData.csv", index=False)
