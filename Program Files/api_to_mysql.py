import requests
import json
import mysql.connector
from datetime import datetime

# Define the MySQL connection parameters
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'DB'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Product (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        slug VARCHAR(255),
        visible BOOLEAN,
        productType VARCHAR(255),
        description TEXT,
        sku VARCHAR(255),
        weight DECIMAL(10, 2),
        stock_trackInventory BOOLEAN,
        stock_inStock BOOLEAN,
        stock_inventoryStatus VARCHAR(255),
        price_currency VARCHAR(255),
        price_price DECIMAL(10, 2),
        price_discountedPrice DECIMAL(10, 2),
        price_formatted_price VARCHAR(255),
        price_formatted_discountedPrice VARCHAR(255),
        priceRange_minValue DECIMAL(10, 2),
        priceRange_maxValue DECIMAL(10, 2),
        costRange_minValue DECIMAL(10, 2),
        costRange_maxValue DECIMAL(10, 2),
        manageVariants BOOLEAN,
        productPageUrl_base VARCHAR(255),
        productPageUrl_path VARCHAR(255),
        numericId VARCHAR(255),
        inventoryItemId VARCHAR(255),
        discount_type VARCHAR(255),
        discount_value DECIMAL(10, 2),
        ribbon VARCHAR(255),
        exportProductId VARCHAR(255),
        lastUpdated DATETIME,
        createdDate DATETIME
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Media (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id VARCHAR(255),
        mediaType VARCHAR(255),
        mainMedia_thumbnail_url VARCHAR(255),
        mainMedia_thumbnail_width INT,
        mainMedia_thumbnail_height INT,
        mainMedia_image_url VARCHAR(255),
        mainMedia_image_width INT,
        mainMedia_image_height INT,
        mainMedia_id VARCHAR(255),
        FOREIGN KEY (product_id) REFERENCES Product(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS MediaItems (
        id INT AUTO_INCREMENT PRIMARY KEY,
        media_id INT,
        thumbnail_url VARCHAR(255),
        thumbnail_width INT,
        thumbnail_height INT,
        mediaType VARCHAR(255),
        title VARCHAR(255),
        image_url VARCHAR(255),
        image_width INT,
        image_height INT,
        image_id VARCHAR(255),
        FOREIGN KEY (media_id) REFERENCES Media(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ProductOptions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id VARCHAR(255),
        optionType VARCHAR(255),
        name VARCHAR(255),
        FOREIGN KEY (product_id) REFERENCES Product(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ProductOptionChoices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_option_id INT,
        value VARCHAR(255),
        description VARCHAR(255),
        inStock BOOLEAN,
        visible BOOLEAN,
        FOREIGN KEY (product_option_id) REFERENCES ProductOptions(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS CollectionIds (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id VARCHAR(255),
        collectionId VARCHAR(255),
        FOREIGN KEY (product_id) REFERENCES Product(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS SEOData (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id VARCHAR(255),
        type VARCHAR(255),
        children VARCHAR(255),
        custom BOOLEAN,
        disabled BOOLEAN,
        props_name VARCHAR(255),
        props_content VARCHAR(255),
        FOREIGN KEY (product_id) REFERENCES Product(id)
    )
""")

# Fetch data from the API
url = "https://www.wixapis.com/stores-reader/v1/products/query"

payload = json.dumps({
  "query": {
    "paging": {
      "limit": 100,
      "offset": 105
    }
  }
})
headers = {
  'wix-site-id': '724e2c86-0001-4ef5-b048-a9646eaf02f7',
  'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcImY0YTU0ZjYxLTQwMDEtNDNiOS1hOGY1LTUyYWYzMDk1MTZhM1wiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImJlOTI2NmVlLTA3MTEtNGExZS1hNDY0LTljMGZjNTE4OWE4Y1wifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCIyMDI5ZjIxNC1hYTdlLTQyMzAtODljOC01MmM0ZTAwMGM0MWRcIn19IiwiaWF0IjoxNzE3NTY5NDg4fQ.S9D_Ae3HyTX_Ybo1z0auuFLQeOrpJip70aBpxUPHHHj0XmhY1EF_Ba4xKCtMeoSrgf74tbzQ83nXCOc2STQAq-em7ZOO4JXC4B4zz4l9gTYWQzgl0Dnkg3bAM4Cc4T78KRIBIOivmOxv-Jo5k7234cyXfy-IebX93P1xtg2wkSScaJI6dGKS3BfFcKt4BFIC-vG7IJepxrPvWeilfqciQe8tQFBYzR4qOftCibmNDM9yMfvJyJfTkgOQIs0gx2c9mUkOmPpNnvMUCeEQ8N3alSCE50mNEDhKx-FJI27nfxH2V8UxwowtRYz_6tFb8yBJyXuO8THl2nqkx6BBuNNCTg',
  'Content-Type': 'application/json',
  'Cookie': 'XSRF-TOKEN=1719931114|07-8IG8FwD2E'
}

response = requests.request("POST", url, headers=headers, data=payload)

# Parse the response JSON
products = response.json()['products']

# Function to parse datetime strings
def parse_datetime(dt_str):
    if dt_str:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return None

# Insert data into tables
for product in products:
    cursor.execute("""
        INSERT INTO Product (
            id, name, slug, visible, productType, description, sku, weight, stock_trackInventory,
            stock_inStock, stock_inventoryStatus, price_currency, price_price, price_discountedPrice,
            price_formatted_price, price_formatted_discountedPrice, priceRange_minValue, priceRange_maxValue,
            costRange_minValue, costRange_maxValue, manageVariants, productPageUrl_base, productPageUrl_path,
            numericId, inventoryItemId, discount_type, discount_value, ribbon, exportProductId, lastUpdated, createdDate
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        product['id'], product['name'], product['slug'], product['visible'], product['productType'], product.get('description', ''),
        product.get('sku', ''), product.get('weight', 0), product['stock'].get('trackInventory', False), product['stock'].get('inStock', False), 
        product['stock'].get('inventoryStatus', ''), product['price'].get('currency', ''), product['price'].get('price', 0), 
        product['price'].get('discountedPrice', 0), product['price']['formatted'].get('price', ''), product['price']['formatted'].get('discountedPrice', ''),
        product['priceRange'].get('minValue', 0), product['priceRange'].get('maxValue', 0), product['costRange'].get('minValue', 0), 
        product['costRange'].get('maxValue', 0), product.get('manageVariants', False), product['productPageUrl'].get('base', ''), 
        product['productPageUrl'].get('path', ''), product.get('numericId', ''), product.get('inventoryItemId', ''), product['discount'].get('type', ''),
        product['discount'].get('value', 0), product.get('ribbon', ''), product.get('exportProductId', ''), parse_datetime(product.get('lastUpdated')), parse_datetime(product.get('createdDate'))
    ))
    
    # Insert Media
    media = product.get('media')
    if media:
        mainMedia = media.get('mainMedia', {})
        cursor.execute("""
            INSERT INTO Media (
                product_id, mediaType, mainMedia_thumbnail_url, mainMedia_thumbnail_width, mainMedia_thumbnail_height,
                mainMedia_image_url, mainMedia_image_width, mainMedia_image_height, mainMedia_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            product['id'], mainMedia.get('mediaType', ''), mainMedia.get('thumbnail', {}).get('url', ''),
            mainMedia.get('thumbnail', {}).get('width', 0), mainMedia.get('thumbnail', {}).get('height', 0), 
            mainMedia.get('image', {}).get('url', ''), mainMedia.get('image', {}).get('width', 0), mainMedia.get('image', {}).get('height', 0),
            mainMedia.get('id', '')
        ))
        media_id = cursor.lastrowid
        
        for item in media.get('items', []):
            cursor.execute("""
                INSERT INTO MediaItems (
                    media_id, thumbnail_url, thumbnail_width, thumbnail_height, mediaType, title, image_url,
                    image_width, image_height, image_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                media_id, item['thumbnail']['url'], item['thumbnail']['width'], item['thumbnail']['height'],
                item['mediaType'], item.get('title', ''), item['image']['url'], item['image']['width'], item['image']['height'],
                item['id']
            ))
    
    # Insert Product Options
    for option in product.get('productOptions', []):
        cursor.execute("""
            INSERT INTO ProductOptions (
                product_id, optionType, name
            ) VALUES (%s, %s, %s)
        """, (product['id'], option['optionType'], option['name']))
        option_id = cursor.lastrowid
        
        for choice in option.get('choices', []):
            cursor.execute("""
                INSERT INTO ProductOptionChoices (
                    product_option_id, value, description, inStock, visible
                ) VALUES (%s, %s, %s, %s, %s)
            """, (option_id, choice['value'], choice['description'], choice.get('inStock', False), choice.get('visible', False)))
    
    # Insert Collection IDs
    for collectionId in product.get('collectionIds', []):
        cursor.execute("""
            INSERT INTO CollectionIds (
                product_id, collectionId
            ) VALUES (%s, %s)
        """, (product['id'], collectionId))
    
    # Insert SEO Data
    for tag in product.get('seoData', {}).get('tags', []):
        cursor.execute("""
            INSERT INTO SEOData (
                product_id, type, children, custom, disabled, props_name, props_content
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            product['id'], tag['type'], tag['children'], tag.get('custom', False), tag.get('disabled', False), 
            tag.get('props', {}).get('name', ''), tag.get('props', {}).get('content', '')
        ))

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data inserted successfully.")
