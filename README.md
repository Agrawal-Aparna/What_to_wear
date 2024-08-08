**Weather Clothing Suggestion App**
**Overview** The Weather Clothing Suggestion App is a Python application that provides personalized clothing recommendations based on real-time weather data in Oslo, Norway. This app helps users dress appropriately for varying weather conditions by suggesting suitable outfits and essential accessories, ensuring comfort and style.

**Features Real-Time Weather Fetching:** Utilizes the Met.no API to retrieve current weather conditions, including temperature, feels-like temperature, and precipitation. 

**Intelligent Outfit Suggestions:** Categorizes clothing options into temperature ranges and suggests tops, bottoms, outerwear, and accessories tailored to the current weather. 

**Layering and Accessories:** Ensures users are prepared for changing temperatures with recommendations for layering and specific accessories, such as gloves and scarves. 

**Easy-to-Update Clothing Database:** Uses a CSV file for defining clothing items, making it simple to customize and expand your wardrobe options. 

**How It Works** 
Fetch Weather Data: The app retrieves real-time weather information for Oslo using the Met.no API. 

Categorize Temperature: Based on the current temperature, the app categorizes clothing options into defined ranges, ensuring appropriate suggestions.

Suggest Outfits: The app provides a selection of tops, bottoms, outerwear, and accessories, tailored to the user’s weather conditions. 

Enhance Your Dressing Experience: Users receive curated outfit recommendations, making it easier to dress for the day ahead. 

Temperature Categories The app categorizes temperature ranges as follows:

Hot: Above 25°C Warm: 15°C to 24.9°C Cool: 5°C to 14.9°C Cold: -5°C to 4.9°C Very Cold: -15°C to -5.1°C Freezing: Below -15°C 

**CSV Data Structure** The clothes.csv file contains the following columns:

Type: The type of clothing (e.g., top, bottom, outerwear, accessory). 
Item: The name of the clothing item. 
Category: The temperature category (e.g., hot, warm, cool, cold, very cold, freezing). 

Contributions are welcome! If you have suggestions for improvements, new features, or any other enhancements, feel free to open an issue or submit a pull request.
