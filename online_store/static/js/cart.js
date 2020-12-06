let updateBtns = document.querySelectorAll('.update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        let product_id = this.dataset.product
        let action = this.dataset.action
        console.log('product_id:', product_id, 'action:', action);

        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            // not logged in
            addCookieItem(product_id, action);
        } else {
            // logged in
            updateUserOrder(product_id, action);
        } 
    })
}




function addCookieItem(product_id, action) {
    console.log('Not logged in..');

    if (action == 'add') {
        if (cart[product_id] == undefined) {
            cart[product_id] = {'quantity': 1};
        } else {
            cart[product_id]['quantity'] += 1;
        } 
    }

    if (action == 'remove') {
        cart[product_id]['quantity'] -= 1;

        if (cart[product_id]['quantity'] <= 0) {
            console.log('Remove item');
            delete cart[product_id];
        } 
    }
    
    if (action == 'delete') {
        console.log('Delete item');
        delete cart[product_id];
    } 

    // update the cookie cart
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}




function updateUserOrder(product_id, action) {
    console.log('User is logged in, sending data..');

    // https://www.brennantymrak.com/articles/fetching-data-with-ajax-and-django.html
    // send post data - Part 3 - 17:00
    let url = '/update_item/';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        // data we're going to send to the backend, as an object
        // but we can't send an object to the backend so we need to send it as a string
        body: JSON.stringify({'product_id': product_id, 'action': action})
    })
    // Fetch doesn't return data directly.
    // It returns a promose that will be fulfilled and resolve to the requested response
    // To get the data from the response, we have to use chained promises by using the .then handler

    // The first promise takes the resolved reponse and converts it to JSON 
    .then(response => {
        return response.json()
    })
    // The second promise gives us access to the data reutrned by the first promise
    // and allow us to use it however we want to update the page 
    .then(data  => {
        console.log('data:', data);
        location.reload()
    })

}

