import os
import time
import requests
import json

def get_completion_with_stats(user_stories, prompt, model="openai/gpt-5-mini", temperature=0):
    REQUESTY_API_KEY = os.getenv("REQUESTY_API_KEY")
    REQUESTY_ENDPOINT = "https://router.requesty.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {REQUESTY_API_KEY}"
    }

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert in creating domain models from given user stories. "
                "I have been given a set of user stories and I need to extract domain models "
                "for the purpose of implementing the software system.\n\n"
                f"User Stories:\n{user_stories}"
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
        "top_p": 1.0,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }

    start_time = time.time()
    response = requests.post(REQUESTY_ENDPOINT, headers=headers, json=payload)
    print("Response",response)
    elapsed = time.time() - start_time

    response_json = response.json()
    print(response_json["choices"][0]["message"])
    output = response_json["choices"][0]["message"]["content"]
    with open("results.txt", "w") as file:
        file.write(output)
    print(response_json["choices"][0]["message"])


    # Requesty typically returns token usage in: response_json["usage"]
    usage = response_json.get("usage", {})

    return {
        "output": output,
        "elapsed_time_sec": elapsed,
        "input_tokens": usage.get("prompt_tokens", None),
        "output_tokens": usage.get("completion_tokens", None),
        "total_tokens": usage.get("total_tokens", None)
    }

if __name__ == '__main__':
    prompt = """
        Find relationships  between the following classes:  ['Customer', 'CustomerServiceRepresentative', 'WarehouseStaff', 'ShippingDepartmentStaff', 'FinanceDepartmentStaff', 'Manager', 'Administrator', 'Product', 'Catalog', 'ShoppingCart', 'Order', 'ShippingAddress', 'ShippingMethod', 'Discount', 'Coupon', 'PaymentDetails', 'OrderConfirmationEmail', 'Return', 'Exchange', 'Inventory', 'ShippingLabel', 'ShippingNotification', 'ShippingCarrier', 'PackingSlip', 'Invoice', 'PaymentRecord', 'FinancialReport', 'OrderStatistics', 'CustomerSatisfaction', 'UserRole', 'AccessRight', 'SystemConfiguration', 'SystemSetting', 'SystemPerformance', 'SystemSecurity']  involved in the user stories.
        Go through each individual user story first, like the examples given below, 
        find the relationships involved in that user story and then 
        collect all the relationships you found in each individual user story.
        Find as many relationships as possible from each user story, 
        ********************************************************
        ✅ Examples of my manually extracted relationships among classes (5 user stories with their corresponding extracted relationships).
        
        As a Kitchen Employee, I want to see the orders with their status, so that I am aware of the progress of each order.
        
        KitchenEmployee sees Order
        Order has Status
        Order has Progress
        
        As a Kitchen Employee, I want to have an overview of all orders at a glance, so that I cannot miss any relevant orders.
        
        KitchenEmployee overviews Order
        Order has Relevance
        
        As a Kitchen Employee, I want to receive only the products of an order, so that I do not get confused by other irrelevant products.
        
        KitchenEmployee receives Product
        Product belongsTo Order
        Product hasRelevanceTo Order
        
        As a Kitchen Employee, I want to see special requests to be shown together with the product they are concerned about, so that I know if I have to prepare a product in a special way 
        
        KitchenEmployee sees Request
        Request concernedAbout Product
        KitchenEmployee prepares Product
        
        As a Kitchen Employee, I want to have the order number shown together with its related products, so that I am aware of which order the products are coming from.
        
        KitchenEmployee isShown OrderNumber
        OrderNumber isRelatedWith Product
        
        NOTE: 
        In the relationship 'KitchenEmployee receives Product'
        KitchenEmployee is class.
        receives is name (of relationship).
        Product is class.
        
        Output the relationships in the following JSON format:
        {
          "relationships": [
               {
                  "name": ,
                  "source": class,
                  "target": class
                },
           ...
        }
        Only output JSON data as per the output format stated above with in {}, nothing else.
        """

    user_stories_list = """
    As a customer, I want to be able to browse the catalog of products.
    As a customer, I want to search for specific products using keywords.
    As a customer, I want to see the availability and pricing of products.
    As a customer, I want to add products to my shopping cart.
    As a customer, I want to view and edit the contents of my shopping cart.
    As a customer, I want to proceed to checkout an order.
    As a customer, I want to choose a shipping address for my order.
    As a customer, I want to select a preferred shipping method for my order.
    As a customer, I want to apply any available discounts or coupons to my order.
    As a customer, I want to provide payment details to complete my order.
    As a customer, I want to receive an order confirmation email.
    As a customer, I want to track the status of my order.
    As a customer, I want to initiate a return or exchange for a product.
    As a customer service representative, I want to view and manage customer orders.
    As a customer service representative, I want to update the status of an order.
    As a customer service representative, I want to provide refund or exchange options to customers.
    As a customer service representative, I want to view customer order histories.
    """
    # user_stories_list = """
    # As a warehouse staff, I want to receive notifications about new orders.
    # As a warehouse staff, I want to pick and pack products for orders.
    # As a warehouse staff, I want to update the inventory when orders are fulfilled.
    # As a warehouse staff, I want to generate shipping labels for orders.
    # As a warehouse staff, I want to notify the shipping department about ready orders.
    # As a shipping department staff, I want to receive shipping notifications.
    # As a shipping department staff, I want to schedule pickups with shipping carriers.
    # As a shipping department staff, I want to update the shipping status of orders.
    # As a shipping department staff, I want to print shipping labels and packing slips.
    # As a finance department staff, I want to generate invoices for orders.
    # As a finance department staff, I want to track payment status and records.
    # As a finance department staff, I want to generate financial reports based on orders.
    # As a manager, I want to view overall order statistics.
    # As a manager, I want to monitor customer satisfaction through order feedback.
    # As a manager, I want to manage user roles and access rights for the Order Processing System.
    # As an administrator, I want to back up and restore the Order Processing System data.
    # As an administrator, I want to manage system configurations and settings.
    # As an administrator, I want to monitor system performance and security.
    # """
    # get_completion_with_stats(user_stories_list,prompt)
    #get_completion_with_stats(user_stories_list,prompt,"deepseek/deepseek-chat")

    #alibaba/qwen-turbo
    #google/gemini-2.0-flash-001
    get_completion_with_stats(user_stories_list, prompt, "google/gemini-2.0-flash-001")