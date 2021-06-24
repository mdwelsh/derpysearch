/* Search result page code */

function hideSpinner() {
    console.log("Hiding spinner");
    $("#searchresultspinner").hide();
}

function addResult(result) {
    console.log("addResult called");
    console.log(result);
    var resultEntry = $("<div>").addClass("resultentry");
    resultEntry.appendTo(".searchresultsresults");
    var urlDiv = $("<div>").addClass("resulturl");
    var urlHost = $("<span>").addClass("resulturlhost").text(result.urlHost);
    var urlPath = $("<span>").addClass("resulturlpath").text(result.urlPath);
    urlDiv.append(urlHost);
    urlDiv.append(urlPath);
    var titleDiv = $("<div>").addClass("resulttitle");
    var titleLink = $("<a>")
        .addClass("resultlink")
        .attr("href", result.link)
        .text(result.title);
    titleDiv.append(titleLink);
    var snippetDiv = $("<div>").addClass("resultsnippet").text(result.snippet);
    resultEntry.append(urlDiv);
    resultEntry.append(titleDiv);
    resultEntry.append(snippetDiv);
}

function showResults(results) {
    results.results.forEach(result => addResult(result));
}

$(function () {
    console.log("Document ready");

    let searchParams = new URLSearchParams(window.location.search);
    let searchTerm = searchParams.get('q');
    console.log("searchTerm: " + searchTerm);

    $.ajax({
        url: "/searchresults?q=" + searchTerm, success: function (result) {
            console.log("Got results: " + result);
            hideSpinner();
            showResults(result);
        }
    });

});

