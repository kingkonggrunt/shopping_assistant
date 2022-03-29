# %%
from saucier import Soup, Utensils
import re

# %%
s = Soup.from_url("https://shop.coles.com.au/a/national/everything/search/milk", 
                  "html5lib")

# %%
d = s.find_all(name="div")

# product
# product product-specials
# div
# product product-every-day
# product has-merch-assoc product-every-day
# product has-flag product-new
# product product-down-down


# %%
for div in d:
    print(div.get('class'))

# %%
print(s)

# %%



