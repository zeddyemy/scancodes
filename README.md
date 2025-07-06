# ScanCodes API

### Response Structure:

**Every API endpoint ensures a consistent response structure comprising:**

- `status` (string): Signifying the request outcome, either "success" or "failed".
- `message` (string): A message that conveys supplementary information regarding the request status
- `status_code` (integer): Represents the HTTP status code, reflecting the success or failure of the request.
- `data` (object): Contains extra data for the specific to individual endpoints.
    

These elements are foundational across all endpoints. For endpoint-specific details, refer to the individual documentation sections.


## Pagination in API Requests
### Overview
When working with large sets of data, our API supports pagination to allow you to retrieve data in chunks (pages) rather than all at once. This helps with performance and makes it easier to manage large datasets on the frontend.

### Requesting Paginated Data
To request paginated data from the API, you will need to include the following query parameters in your request:

- `page` (optional): The page number you want to retrieve. Defaults to 1 if not specified.
- `per_page` (optional): The number of items to retrieve per page. Defaults to 10 if not specified.

### Example Request
```http
GET /api/resource?page=2&per_page=15
```
- `page=2`: This will return the second page of results.
- `per_page=15`: This will return 15 items per page.


### Understanding the Paginated Response
The API will return the data in a paginated format, which includes metadata about the pagination, along with the data for the requested page.

### Example Response
```json
{
    "current_page": 2,
    "total": 145,
    "total_pages": 10,
    "data": [
        {
            "id": 16,
            "name": "Item 16",
            "description": "Description for item 16"
        },
        {
            "id": 17,
            "name": "Item 17",
            "description": "Description for item 17"
        },
        // 13 more items...
    ]
}
```

### Response Fields:
- `current_page`: The current page number you are viewing.
- `total`: The total number of items across all pages.
- `total_pages`: The total number of pages available.
- `data`: An array containing the data for the current page.

## Implementing Pagination on the Frontend

1. **Initial Data Load:**
    - Start by loading the first page of data `(page=1)`.
    - Display the data on the frontend.

2. **Navigating Between Pages:**

    - Use the `total_pages` field from the response to determine the number of pages available.
    - Implement buttons or links for "Next", "Previous", "First", and "Last" page navigation.
    - Update the `current_page` parameter in the API request when navigating between pages.

3. **Handling Edge Cases:**

    - **Empty Data:** If the `data` array is empty, this means there are no items for that page.
    - **Invalid Page Numbers:** If the user tries to navigate to a page beyond the `total_pages`, handle this gracefully by either showing a message or redirecting them to a valid page.

### Example Usage on the Frontend

```javascript
async function fetchPaginatedData(page = 1, perPage = 10) {
    const response = await fetch(`/api/resource?page=${page}&per_page=${perPage}`);
    const result = await response.json();

    // Handle the data
    displayData(result.data);

    // Update pagination UI based on result.page and result.total_pages
    updatePagination(result.page, result.total_pages);
}

function displayData(data) {
    // Code to render data on the frontend
}

function updatePagination(currentPage, totalPages) {
    // Code to update pagination controls (next, previous, etc.)
}
```

## Tips for Implementation
- **Optimizing Performance:** Load data for the next page in the background while the user is viewing the current page to make transitions smoother.
- **State Management:** Keep track of the current page in your application's state to ensure the UI reflects the correct page after navigation.