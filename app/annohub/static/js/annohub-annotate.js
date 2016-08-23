function renderValues(token, annotation){
    var doc = document.getElementById("annotation-text");
    var this_html = [];

    //console.log("rendering");
    //console.log(token);

    /*doc.innerHTML = "";*/
    for (i=0; i < token.length; i++){
        //console.log(token[i]);
        //console.log(token[i].length);
        if (token[i].length > 0){
            this_html.push("<div data-sent=\"" + i + "\" class=\"sent\">");
            for (j=0; j < token[i].length; j++){
                //console.log(token[i][j]);
                //console.log(i[j]);
                this_html.push("<span class=\"pair\"><span data-token=\"" + j + "\" class=\"token\">");
                this_html.push(token[i][j]);
                this_html.push("</span>");

                this_html.push("<span data-annotation=\"" + j + "\" class=\"annotation\">");
                this_html.push(annotation[i][j]);
                this_html.push("</span></span>");
            }
            this_html.push("</div>");
        }
    }
    doc.innerHTML = this_html.join("");
    //console.log(this_html.join(""));
}

function setID(project){
    //console.log("setting");
    return $('#annotation-text').data('project', project);
}

function getID(){
    //console.log("getting");
    return $('#annotation-text').data('project');
}

function getValues(){
    return $('#annotation-text').data('tags');
}

function getTag(tags, tag) {
  for (var i=0, length=tags.length; i<length; i++) {
    if (tags[i].key == tag.toUpperCase()) return tags[i];
  }
  return false;
}

function setInactiveKeys(){
    $('.activeKey').removeClass('activeKey');
}

function setActiveKey(element){
    $(element).addClass('activeKey');
}

function getActiveKey(){
    return $('.activeKey').first().text();
}

function setTagInfo(result){
    if (result === false){
        //console.log(result);
        //$('.hidden').hide();
        $('.annotation-header').css('visibility','hidden');
        $('.annotation-value').css('visibility','hidden');
    } else {
        $('#annotation-key').text(result.key);
        $('#annotation-description').text(result.description);
        $('#annotation-example').text(result.example);
        $('.ellipsis').css('overflow', 'hidden');
        $('.annotation-header').css('visibility','visible');
        $('.annotation-value').css('visibility','visible');
        //$('.hidden').show();
    }
    setInactiveKeys();
}

function increment(ret){
    if (ret[0] === false && ret[1] === false){
        return [false, false];
    }
    var all_sent = $('#annotation-text').children();
    if (ret[0] < all_sent.length){
        //console.log(all_sent.eq(ret[0]).children().eq(ret[1]).text());
        if (ret[1] + 1 < all_sent.eq(ret[0]).children().length){
            //console.log("true inc pos");
            return [ret[0], (ret[1] + 1)];
        } else {
            if (ret[0] + 1 < all_sent.length){
                //console.log("true inc sent");
                return [ret[0] + 1, 0];
            } else {
                //console.log("pos is last sentence end");
                return [false, false];
            }
        }
    } else {
        //console.log("got last sentence end");
        return [false, false];
    }
}
function highlightSentpos(ret){
    //console.log(ret[0] + " " + ret[1]);
    $('.activePair').removeClass('activePair');
    $('#annotation-text').children().eq(ret[0]).children().eq(ret[1]).addClass('activePair');
}

function afterIncrement(tags){
    // info about new tag
    var tag = $('.activePair').children().last().text();
    var result = getTag(tags, tag);
    setTagInfo(result);
}

function clearInput(this_list){
    // clear search
    $('#annotation-search').val('');
    // trigger list reset
    this_list.search();
    $('.activePair').removeClass('activePair');
}

function setNewTag(ret, tag, tags, annotation){
    // set a new tag for the currently active field and jump to the next one
    // return the data
    if (tag !== false && tag !== "" && tag !== undefined){
        $('.activePair').children().last().text(tag);
        annotation[ret[0]][ret[1]] = tag;
        //$('#annotation-text').children().eq(ret[0]).children().eq(ret[1]).text(tag);
    }
    return annotation;
}

function selectNext(ret, tags, annotation_list){
    // a wrapper function for selecting the next tag
    ret = increment(ret);
    clearInput(annotation_list);
    highlightSentpos(ret);
    afterIncrement(tags);
    return ret;
}

