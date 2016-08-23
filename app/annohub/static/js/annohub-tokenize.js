//var values = JSON.parse('[[1, "abc", 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]');
//var values = JSON.parse('[[1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2]]');

function renderValues(values){
    var doc = document.getElementById("tokenizing-text");
    this_html = [];

    //console.log("rendering");
    //console.log(values);

    /*doc.innerHTML = "";*/
    for (i=0; i < values.length; i++){
        //console.log(values[i]);
        //console.log(values[i].length);
        if (values[i].length > 0){
            this_html.push("<p><span data-sent=\"" + i + "\" class=\"sent\">");
            for (j=0; j < values[i].length; j++){
                //console.log(values[i][j]);
                //console.log(i[j]);
                this_html.push("<span data-token=\"" + j + "\" class=\"token\">");
                this_html.push(values[i][j]);
                this_html.push("</span>");
            }
            this_html.push("</span></p>");
        }
    }
    doc.innerHTML = this_html.join("");
    //console.log(this_html.join(""));
}

function setValues(values){
    //console.log("setting");
    return $('#tokenizing-text').data('text', values);
}

function setID(project){
    //console.log("setting");
    return $('#tokenizing-text').data('project', project);
}

function getID(){
    //console.log("getting");
    return $('#tokenizing-text').data('project');
}

function getValues(){
    //console.log("getting");
    return $('#tokenizing-text').data('text');
}

// actions for nouns
function deleteEntity(values, noun, token, sent){
    if (noun == 'sent'){
        values.splice(sent, 1);
    } else if (noun == 'token'){
        values[sent].splice(token, 1);
    } else if (noun == 'punct'){
        values[sent][token] = values[sent][token].replace(/^([\W_])+|([\W_])+$/g,'');
        if (values[sent][token].length === 0){
            deleteEntity(values, 'token', token, sent);
        }
    }
    return values;
}

function joinEntity(values, noun, token, sent){

    if (noun == 'sent'){
        //console.log(values.length);
        if ((sent + 1) < values.length){
            //console.log("True!");
            values[sent] = values[sent].concat(values[sent+1]);
            values = deleteEntity(values, noun, token, sent + 1);
        }
        //console.log(values.length);
    } else if (noun == 'token'){
        if ((token + 1) < values[sent].length){
            values[sent][token] = String(values[sent][token]) + " " + String(values[sent][token + 1]);
            values = deleteEntity(values, noun, token + 1, sent);
        }
    } else if (noun == 'punct'){
        if ((token + 1) < values[sent].length && values[sent][token].match(/^[^A-Za-z0-9\s]$/)){
            values[sent][token] = String(values[sent][token]) + "" + String(values[sent][token + 1]);
            values = deleteEntity(values, 'token', token + 1, sent);
        }
    }
    return values;
}

function splitEntity(values, noun, token, sent){
    if (noun == 'sent'){
        if (token < (values[sent].length - 1) ){
            sentence_rest = values[sent].slice(token + 1);
            values[sent] = values[sent].slice(0, token + 1);
            values.splice(sent + 1, 0, sentence_rest);
        }
    } else if (noun == 'token'){
        sub_strings = String(values[sent][token]).split(/\s+/);
        if (sub_strings.length > 1){
            //console.log(sub_strings.apply);
            first = sub_strings.shift();
            values[sent].splice(token, 1, first);
            for (i=0; i<sub_strings.length; i++){
                values[sent].splice(token+i+1, 0, sub_strings[i]);
            }
        }
    } else if (noun == 'punct'){
        sub_strings = String(values[sent][token]).split(/^([^A-Za-z0-9\s])|([^A-Za-z0-9\s])$/g);
        sub_strings = sub_strings.filter(function(n){ return n !== undefined && n !== "";});
        //console.log(sub_strings);
        if (sub_strings.length > 1){
            first = sub_strings.shift();
            values[sent].splice(token, 1, first);
            for (i=0; i<sub_strings.length; i++){
                values[sent].splice(token+i+1, 0, sub_strings[i]);
            }
        }
    }
    return values;
}

function doAction(token, sent, verb, noun){

    var values = getValues();

    if ((!(typeof verb === 'string' || verb instanceof String)) ||
    (!(typeof noun === 'string' || noun instanceof String))){
        return false;
    }
    if ((!(typeof token === 'number' || token instanceof Number)) ||
    (!(typeof sent === 'number' || sent instanceof Number))){
        return false;
    }

    switch (verb) {
        case 'delete':
            values = deleteEntity(values, noun, token, sent);
            break;
        case 'split':
            values = splitEntity(values, noun, token, sent);
            break;
        case 'join':
            values = joinEntity(values, noun, token, sent);
            break;
        default:
    }
    setValues(values);
    return true;
}

function main(token, sent, verb, noun){
    doAction(token, sent, verb, noun);
    renderValues(getValues());
}

function getVerb(){
    return $("#tokenizing-verb label.active input").attr('id');
}

function getNoun(){
    return $("#tokenizing-noun label.active input").attr('id');
}


