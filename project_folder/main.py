import pandas as pd

# Load the dummy data
data = pd.read_csv("/Users/ishworthapa/Dropbox/Mac/Documents/Freelancing/Freelance_Pythin/Freelance_Portfolio/data/dummy_data.csv")



# Handle missing 'Age' values by filling with the mean age
data['Age'] = data['Age'].fillna(int(data['Age'].mean()))

# Standardize phone numbers (add +977 if missing and format it)
def format_phone_number(phone):
    phone = ''.join(filter(str.isdigit, str(phone)))  # Remove non-digit characters
    if phone.startswith('977'):
        return f"+977-{phone[3:]}"  # Format it with '+977-'
    elif len(phone) == 10:  # If it’s a local number (10 digits), add +977 country code
        return f"+977-{phone}"
    return phone  # Return as is if already formatted

# Apply phone number formatting
data['Phone'] = data['Phone'].apply(format_phone_number)


# Step 1: Fill missing values based on matching Name, Age, or Email
# We'll first group by 'Name' and 'Age' to get rows that likely belong to the same person
data['Phone'] = data.groupby(['Name', 'Age', 'Email'])['Phone'].transform('first')

# Step 2: Now, fill missing 'Email' if the same Name and Age coincide
data['Email'] = data.groupby(['Name', 'Age'])['Email'].transform('first')

# Step 3: Handle missing 'Phone' values based on matching 'Name' and 'Age'
data['Phone'] = data.groupby(['Name', 'Age'])['Phone'].transform('first')

# Step 4: Handle missing 'Age' values based on matching 'Name' and 'Email'
data['Age'] = data.groupby(['Name','Email'])['Age'].transform('first')

# Handle missing 'Name' by filling with "Unknown" or you can drop the row
data['Name'] = data['Name'].fillna('Unknown')

# Handle missing 'Email' by filling with "missing_email@example.com"
data['Email'] = data['Email'].fillna('missing_email@example.com')
# Remove any remaining duplicates if needed
data = data.drop_duplicates()

# Save the cleaned data
data.to_csv("cleaned_data.csv", index=False)
print("Data cleaning complete.")
