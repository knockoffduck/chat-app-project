//Get search input element
const search = document.querySelector('#search');

//Initial placeholder
const initial = search.placeholder;

//Add focus event listener to search
search.addEventListener('focus', function(){
    //Clear placeholder value
    search.placeholder = '';
});

//Add blur event listener to search
search.addEventListener('blur', function(){
    //Restore initial placeholder when input loses focus
    search.placeholder = initial;
})