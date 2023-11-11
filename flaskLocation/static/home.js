function toggleSortingOptions() {
    var selectionInput = document.getElementById('selectionInput');
    var sortingOptions = document.getElementById('ebay')
    if (selectionInput.value === "1") {
        sortingOptions.style.display = 'block';
    } else {
        sortingOptions.style.display = 'none';
    }
}

function updateSliderInput(val) {
    //update numerical value of slider as it's dragged. 
    //currently unknown what number user is sliding.
    document.getElementById('')
}