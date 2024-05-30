let previousScene = 1;

let numberchat = 0;
let numberchatactuel = 0;

$(document).ready(function() {
    initializeScene(previousScene);
    // Initialiser la première scène
});

function changeScene(sectionNumber) {
    // Arrêter et nettoyer la scène précédente s'il y en a une
    if (previousScene) {
        stopScene(previousScene);
    }
    // Initialiser la nouvelle scène
    initializeScene(sectionNumber);
    // Mettre à jour la référence de la scène précédente
    previousScene = sectionNumber;
}

function stopScene(sceneNumber) {
    switch (sceneNumber) {
        case 1:
            stopScene1();
            break;
        case 2:
            stopScene2();
            break;
        case 3:
            stopScene3();
            break;
        default:
            console.error("Scene not supported");
            break;
    }
}

function stopScene1() {
    let container = document.querySelector('.app_container_page1');
    if (container) {
        container.remove();
    }
}

function stopScene2() {
    let containerPage2 = document.querySelector('.app_container_page');
    if (containerPage2) {
        containerPage2.remove();
    }
}

function stopScene3() {
    let containerPage2 = document.querySelector('.app_container_page');
    if (containerPage2) {
        containerPage2.remove();
    }
}

function initializeScene(sectionNumber) {
    switch (sectionNumber) {
        case 1:
            initializeScene1();
            break;
        case 2:
            initializeScene2();
            break;
        case 3:
            initializeScene3();
            break;
        default:
            console.error("Section not supported");
            break;
    }
}

function initializeScene1() {
    let container = document.createElement('div');
    container.className = 'app_container_page1';

    let leftSection = document.createElement('div');
    leftSection.className = 'left-section';

    let appName = document.createElement('img');
    appName.src = 'static/img/logo.png';
    appName.className = 'appName';
    appName.alt = 'Text AI Logo';
    leftSection.appendChild(appName);

    let separator = document.createElement('div');
    separator.className = 'separator';
    leftSection.appendChild(separator);

    let title = document.createElement('h1');
    title.className = 'title_page1';
    title.textContent = 'Discover the world of movies and TV series without effort, thanks to our artificial intelligence.';
    leftSection.appendChild(title);

    let button = document.createElement('button');
    button.className = 'btn-page1';

    let buttonText = document.createElement('h1');
    buttonText.className = 'btn-text-page1';
    buttonText.textContent = 'Try It!';
    button.appendChild(buttonText);

    leftSection.appendChild(button);
    container.appendChild(leftSection);

    let rightSection = document.createElement('div');
    rightSection.className = 'right-section';

    let details = document.createElement('div');
    details.className = 'details_page1';

        // Ajout du logo en bas à droite
        let bottomRightLogo = document.createElement('img');
        bottomRightLogo.src = 'static/img/logo_dell.png';
        bottomRightLogo.alt = 'Bottom Right Logo';
        bottomRightLogo.className = 'bottom-right-logo';
        rightSection.appendChild(bottomRightLogo);
            

    let p = document.createElement('p');
    p.className = 'p_page1';
    p.innerHTML = 'Programmed by <strong>interns</strong> from the <strong>MIASHS License at Paul Valéry University</strong>, <strong>FlickFriend</strong> is a chatBot based on Llama 3 LLM';
    details.appendChild(p);

    let img = document.createElement('img');
    img.src = 'static/img/univ2.png';
    img.alt = 'AI Image';
    img.className = 'img_univ';
    details.appendChild(img);


    rightSection.appendChild(details);
    container.appendChild(rightSection);

    document.body.appendChild(container);

    // gsap.from('.btn-page1', { duration: 1, y: -100, opacity: 0, ease: 'back.out(1.7)' });

    $('.btn-page1').click(function() {
        changeScene(2);
    });
}




function initializeScene2() {

    // Conteneur principal pour la page 2
    const containerPage2 = document.createElement('div');
    containerPage2.className = 'app_container_page';

    // Création du header de la page 2
    const page2Header = document.createElement('div');
    page2Header.className = 'page2_header';

    // Ajout du logo
    const logoImg = document.createElement('img');
    logoImg.src = 'static/img/logo_dell.png';
    logoImg.alt = 'Dell Logo';
    logoImg.className = 'page2_logo';
    page2Header.appendChild(logoImg);
    
    // gsap.from(appName, {duration: 1, x:-100,opacity: 0, ease: 'back.out(1.7)'});

    // Création du conteneur pour les liens
    const linkHeader = document.createElement('div');
    linkHeader.className = 'linkHeader';

    // Boutons Home et About
    const linkHome = document.createElement('button');
    linkHome.className = 'linkHome';
    linkHome.innerHTML = '<p>Home</p>';
    linkHeader.appendChild(linkHome);

    const linkAbout = document.createElement('button');
    linkAbout.className = 'linkAbout';
    linkAbout.innerHTML = '<p>About</p>';
    linkHeader.appendChild(linkAbout);

    page2Header.appendChild(linkHeader);
    containerPage2.appendChild(page2Header);

    // Création du contenu de la page 2
    const page2Content = document.createElement('div');
    page2Content.className = 'page2_content';

    // Contenu gauche
    const page2ContentLeft = document.createElement('div');
    page2ContentLeft.className = 'page2_content_left active';

    const menuHistoryClose = document.createElement('img');
    menuHistoryClose.src = 'static/img/menu-close.png';
    menuHistoryClose.alt = 'menu-close';
    menuHistoryClose.className = 'menuHistoryClose';
    page2ContentLeft.appendChild(menuHistoryClose);

    const contentTitle = document.createElement('h1');
    contentTitle.className = 'page2_content_title';
    contentTitle.textContent = 'History';
    page2ContentLeft.appendChild(contentTitle);

    const line = document.createElement('div');
    line.className = 'line';
    page2ContentLeft.appendChild(line);

    const historyContent = document.createElement('div');
    historyContent.className = 'page2_content_history';
    page2ContentLeft.appendChild(historyContent);

    page2Content.appendChild(page2ContentLeft);

    // Contenu droit
    const page2ContentRight = document.createElement('div');
    page2ContentRight.className = 'page2_content_right';

    const menuHistoryOpen = document.createElement('img');
    menuHistoryOpen.src = 'static/img/menu.png';
    menuHistoryOpen.alt = 'menu-open';
    menuHistoryOpen.className = 'menuHistoryOpen';
    page2ContentRight.appendChild(menuHistoryOpen);

    const contentChoice = document.createElement('div');
    contentChoice.className = 'page2_content_choice';

    const choice = document.createElement('div');
    choice.className = 'choice';

    // Ajout du logo de l'assistant
    const assistantLogo = document.createElement('img');
    assistantLogo.src = 'static/img/assistant.png';
    assistantLogo.alt = 'Assistant Logo';
    assistantLogo.className = 'assistant';

    const choiceText = document.createElement('p');
    choiceText.className = 'choiceText';
    choiceText.textContent = "Hello, I'm FlickFriend, your assistant for this chat, can you choose the mode you want :";

    const choiceButtons = document.createElement('div');
    choiceButtons.className = 'choiceButtons';
    const choiceButton1 = document.createElement('button');
    choiceButton1.className = 'choiceButton';
    choiceButton1.textContent = 'Movie';
    const choiceButton2 = document.createElement('button');
    choiceButton2.className = 'choiceButton';
    choiceButton2.textContent = 'Series';
    const choiceButton3 = document.createElement('button');
    choiceButton3.className = 'choiceButton';
    choiceButton3.textContent = 'People';

    choice.appendChild(assistantLogo);
    choice.appendChild(choiceText);
    choice.appendChild(choiceButtons);
    choiceButtons.appendChild(choiceButton1);
    choiceButtons.appendChild(choiceButton2);
    choiceButtons.appendChild(choiceButton3);

    contentChoice.appendChild(choice);
    page2ContentRight.appendChild(contentChoice);
    page2Content.appendChild(page2ContentRight);
    containerPage2.appendChild(page2Content);


    // Bas de page
    const page2Bottom = document.createElement('div');
    page2Bottom.className = 'page2_bottom';

    
    containerPage2.appendChild(page2Bottom);

    // Ajout du conteneur principal à la page
    document.body.appendChild(containerPage2);  
    loadConversationTitles();

    $.ajax({
        url: '/count_conversations',
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            numberchat = response.num_files;
            numberchatactuel = numberchat;
            console.log('Number of conversation files:', numberchat);
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });



    $('.page2_logo').click(function() {
        // Changer de scène
        changeScene(1);
    });
    $('.linkHome').click(function() {
        // Changer de scène
        changeScene(2);
    });
    $('.linkAbout').click(function() {
        // Changer de scène
        changeScene(3);
    });


    $('.menuHistoryClose').click(function() {
        $('.page2_content_left').toggleClass('active');
        $(".menuHistoryOpen").toggleClass('active');

    });
    $('.menuHistoryOpen').click(function() {
        $('.page2_content_left').toggleClass('active');
        $(".menuHistoryOpen").toggleClass('active');

    });

    $('.choiceButton').click(function() {
        var buttonText = $(this).text();
        localStorage.setItem('mode', buttonText);
        console.log(buttonText);   // Affiche le texte du bouton dans la console (pour vérification)
        $(contentChoice).remove();
        createConversation(buttonText);
        createDropdown(buttonText);
        dropdownAnim();

        const imageFond = document.createElement('img');
        imageFond.src = 'static/img/logo_fond.png';
        imageFond.alt = 'Logo';
        imageFond.className = 'logoFond';
        page2ContentRight.appendChild(imageFond);
        const zoneMessages = document.createElement('div');
        zoneMessages.className = 'zone-messages';
        page2ContentRight.appendChild(zoneMessages);

        const  buttonNewChat = document.createElement('button');
        buttonNewChat.className = 'buttonNewChat';
        buttonNewChat.textContent = 'New Chat';
        page2Bottom.appendChild(buttonNewChat);

        const topButton = document.createElement('button');
        topButton.className = 'scrollToTopButton';
        topButton.textContent = 'Top';
        page2ContentRight.appendChild(topButton);

        const jsonOutput = document.createElement('pre');
        jsonOutput.id = 'jsonOutput';
        page2ContentRight.appendChild(jsonOutput);

        const chatText = document.createElement('div');
        chatText.className = 'chatText';

        const chatInput = document.createElement('input');
        chatInput.type = 'text';
        chatInput.className = 'chatInput';
        chatInput.placeholder = 'Type a message...';
        chatText.appendChild(chatInput);

        const chatSend = document.createElement('button');
        chatSend.className = 'chatSend';
        chatSend.textContent = 'Send';
        chatText.appendChild(chatSend);

        const attention = document.createElement('p');
        attention.className = 'attention';
        attention.textContent = 'FlickFriend can make mistakes. Consider checking important information.';

        page2Bottom.appendChild(chatText);
        document.querySelector(".app_container_page").appendChild(attention);


        $('.buttonNewChat').click(function() {            
            const content = $('.zone-messages').html();

        
            $.ajax({
                url: '/save_conversation',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ content: content, numberchat: numberchatactuel }),
                success: function(response) {

                    changeScene(2);
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                    alert('Failed to save conversation.');
                }
            });
        });

        $('.scrollToTopButton').click(function() {
            scrollToTop();
        });

        $('.chatInput').keydown(function(event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                sendMessage();
            }
        });
    
        $('.chatSend').click(function() {
            sendMessage();
        });

    });

}


function initializeScene3(){
    // Element de la scène 
    function createAboutContent(parentElement, title, subTitle1, text1, subTitle2, text2) {
        const titleElement = document.createElement('h1');
        titleElement.className = 'page2_content_title_about';
        titleElement.textContent = title;
        parentElement.appendChild(titleElement);

        const line = document.createElement('div');
        line.className = 'line';
        parentElement.appendChild(line);

        const content = document.createElement('div');
        content.className = 'page2_content_about';

        const p1 = document.createElement('p');
        p1.innerHTML = `<strong>${subTitle1}</strong>`;
        const p2 = document.createElement('p');
        p2.textContent = text1;
        const p3 = document.createElement('p');
        p3.innerHTML = `<strong>${subTitle2}</strong>`;
        const p4 = document.createElement('p');
        p4.textContent = text2;

        content.appendChild(p1);
        content.appendChild(p2);
        content.appendChild(p3);
        content.appendChild(p4);
        parentElement.appendChild(content);
    }

    function createMethodologyContent(parentElement) {
        const title = document.createElement('h1');
        title.className = 'page2_content_title_about';
        title.textContent = 'Methodology and approach';
        parentElement.appendChild(title);

        const line = document.createElement('div');
        line.className = 'line';
        parentElement.appendChild(line);

        const content = document.createElement('div');
        content.className = 'page2_content_about';

        const p1 = document.createElement('p');
        p1.textContent = 'We decided to develop our model using a multi-agent system. This approach divides complex tasks into sub-tasks managed by specialized agents, each with distinct roles.';
        content.appendChild(p1);

        const subTitle = document.createElement('p');
        subTitle.className = 'section-title';
        subTitle.textContent = 'Multi-agent system components';
        content.appendChild(subTitle);

        const ul = document.createElement('ul');
        ul.className = 'list';
        const li1 = document.createElement('li');
        li1.innerHTML = '<strong>Agents:</strong> Responsible for specific tasks such as text generation, query management or data analysis.';
        const li2 = document.createElement('li');
        li2.innerHTML = '<strong>Tools:</strong> Specialized modules used by agents to accomplish their tasks, e.g., connecting to and querying the TMDB (The Movie Database).';
        const li3 = document.createElement('li');
        li3.innerHTML = '<strong>Supervisors:</strong> Coordinate agents and tools to ensure smooth communication and efficient query processing.';
        ul.appendChild(li1);
        ul.appendChild(li2);
        ul.appendChild(li3);
        content.appendChild(ul);

        const p2 = document.createElement('p');
        p2.textContent = 'To enrich our model and generate relevant texts, we integrate queries to the TMDB database, which offers a vast collection of information on films, TV series and film personalities.';
        content.appendChild(p2);

        parentElement.appendChild(content);
    }

    // Création du conteneur principal
    const container = document.createElement('div');
    container.className = 'app_container_page';

    // Création de l'en-tête de la page
    const header = document.createElement('div');
    header.className = 'page2_header';

    const logo = document.createElement('img');
    logo.src = 'static/img/logo_dell.png';
    logo.alt = 'Dell Logo';
    logo.className = 'page2_logo';
    header.appendChild(logo);

    const appName = document.createElement('img');
    appName.src = 'static/img/logo.png';
    appName.className = 'appLogo';
    appName.textContent = 'Text AI';
    header.appendChild(appName);

    const linkHeader = document.createElement('div');
    linkHeader.className = 'linkHeader';

    const linkHome = document.createElement('button');
    linkHome.className = 'linkHome';
    linkHome.innerHTML = '<p>Home</p>';
    linkHeader.appendChild(linkHome);

    const linkAbout = document.createElement('button');
    linkAbout.className = 'linkAbout';
    linkAbout.innerHTML = '<p>About</p>';
    linkHeader.appendChild(linkAbout);

    header.appendChild(linkHeader);
    container.appendChild(header);

    // Création de la section About
    const aboutSection = document.createElement('div');
    aboutSection.className = 'page2_about';

    // Contenu About Us
    const aboutContent1 = document.createElement('div');
    aboutContent1.className = 'page2_about_content';
    createAboutContent(aboutContent1, 'About Us', 'Who are we?', 'We\'re Malcom and Cassandra, two students in the MIASHS (Mathématiques et Informatique Appliquées aux Sciences Humaines et Sociales) Licence 3 program at Montpellier\'s Paul Valéry University. Passionate about artificial intelligence and its applications, we decided to devote our internship to an ambitious and innovative project.', 'Our internship topic', 'The subject of our internship is the creation of a generative artificial intelligence for text generation. The aim of this project is to develop a model capable of producing coherent, relevant texts in a variety of contexts. We could use and draw inspiration from several existing models, such as gpt-3 or mistral Ai.');
    aboutSection.appendChild(aboutContent1);

    // Contenu Methodology
    const aboutContent2 = document.createElement('div');
    aboutContent2.className = 'page2_about_content';
    createMethodologyContent(aboutContent2);
    aboutSection.appendChild(aboutContent2);

    container.appendChild(aboutSection);
    document.body.appendChild(container); 

    
    $('.page2_logo').click(function() {
        // Changer de scène
        changeScene(1);
    });
    $('.linkHome').click(function() {
        // Changer de scène
        changeScene(2);
    });
    $('.linkAbout').click(function() {
        // Changer de scène
        changeScene(3);
    });

}
  
function createDropdown(activeOption) {
    const dropdownContainer = document.querySelector('.page2_content_right');
    // Créer les éléments HTML
    const container = document.createElement('div');
    container.className = 'dropdown-container';
    const dropdown = document.createElement('div');
    dropdown.className = 'dropdown';
    const select = document.createElement('div');
    select.className = 'select';
    const selected = document.createElement('span');
    selected.className = 'selected';
    selected.setAttribute('data-type', 'type');
    selected.setAttribute('data-value', activeOption);
    selected.textContent = activeOption;
    const caret = document.createElement('div');
    caret.className = 'caret';
    select.appendChild(selected);
    select.appendChild(caret);
    const menu = document.createElement('ul');
    menu.className = 'menu';
    const options = [
        { value: 'movie', text: 'Movie' },
        { value: 'series', text: 'Series' },
        { value: 'people', text: 'People' }
    ];
    options.forEach(option => {
        const li = document.createElement('li');
        li.setAttribute('data-value', option.value);
        li.textContent = option.text;
        if (option.value === activeOption) {
            li.className = 'activedrop';
        }
        menu.appendChild(li);
    });
    dropdown.appendChild(select);
    dropdown.appendChild(menu);
    container.appendChild(dropdown);
    dropdownContainer.appendChild(container);
    // Fermer le menu si on clique en dehors
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove('open');
        }
    });
}

function dropdownAnim() {
    const dropdowns = document.querySelectorAll(".dropdown");
    dropdowns.forEach(dropdown => {
        const select = dropdown.querySelector(".select");
        const caret = dropdown.querySelector(".caret");
        const selected = dropdown.querySelector(".selected");
        select.addEventListener("click", () => {
            const menu = dropdown.querySelector(".menu");
            const options = dropdown.querySelectorAll(".menu li");
            select.classList.toggle("select-clicked");
            caret.classList.toggle("caret-rotate");
            menu.classList.toggle("menu-open");
            options.forEach(option => {
                option.addEventListener("click", () => {
                    selected.innerText = option.innerText;
                    localStorage.setItem('mode', option.innerText);
                    selected.setAttribute('data-value', option.getAttribute("data-value"));
                    select.classList.remove("select-clicked");
                    caret.classList.remove("caret-rotate");
                    menu.classList.remove("menu-open");

                    options.forEach(opt => {
                        opt.classList.remove("activedrop");
                    });
                    option.classList.add("activedrop");
                });
            });
        });
    });
}

function scrollToBottom() {
    const zoneMessages = document.querySelector('.zone-messages');
    zoneMessages.scrollTop = zoneMessages.scrollHeight;
}

 function scrollToTop() {
    const zoneMessages = document.querySelector('.zone-messages');
    zoneMessages.scrollTop = 0;
}

function sendMessage() {
    const message = $('.chatInput').val();
    if (message.trim() !== '') {

        const input = $('.chatInput').val();
        const mode = localStorage.getItem('mode');
        addMessageHuman(message, mode);

        $.ajax({
            url: '/process_input',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ input: input, mode: mode }),
            success: function(response) {
                addMessageBot(response.output, mode);
                $('.chatInput').val('');
                const content = $('.zone-messages').html();
                $.ajax({
                    url: '/save_conversation',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ content: content, numberchat: numberchatactuel }),
                    success: function(response) {

                    },
                    error: function(xhr, status, error) {
                        console.error('Error:', error);
                        alert('Failed to save conversation.');
                    }
                });
                
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });


    }
}

function addMessageHuman(message, dataValue ) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.setAttribute('data-value', dataValue);
    
    const messageHumain = document.createElement('div');
    messageHumain.className = 'human-message';

    const messageText = document.createElement('p');
    messageText.className = 'human-message-text';
    messageText.textContent = message;

    messageHumain.appendChild(messageText);
    messageDiv.appendChild(messageHumain);

    $('.zone-messages').append(messageDiv);

    scrollToBottom();
}

function addMessageBot(message, dataValue) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.setAttribute('data-value', dataValue);

    const messageBot = document.createElement('div');
    messageBot.className = 'bot-message';

    const messageText = document.createElement('p');
    messageText.className = 'bot-message-text';
    messageText.textContent = message;

    const detailBot = document.createElement('button');
    detailBot.className = 'detailBot';
    detailBot.textContent = 'Details';

    messageBot.appendChild(messageText);
    messageBot.appendChild(detailBot);
    messageDiv.appendChild(messageBot);

    $('.zone-messages').append(messageDiv);

    scrollToBottom();


    $.ajax({
        url: '/load_json',
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            const article = document.createElement('article');  
            article.className = 'article';       
            messageDiv.appendChild(article);
            if (dataValue === 'Movie') {
                createArticleMovie(response);
            } else if (dataValue === 'People') {
                createArticlePerson(response);
            } else if (dataValue === 'Series') {
                createArticleSeries(response);
            } 
            $(detailBot).click(function() {
                $(article).toggle("active");
            });

        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });

 
}

// FONCTIONS DES ARTICLES
function createArticleMovie(jsonData) {
    const container = document.createElement('div');
    container.className = 'container_movie';

    const poster = document.createElement('div');
    poster.className = 'poster_movie';
    
    const posterImg = document.createElement('img');
    posterImg.src = `https://image.tmdb.org/t/p/w500${jsonData.details.poster_path}`;
    poster.appendChild(posterImg);

    const details = document.createElement('div');
    details.className = 'details_movie';

    const header = document.createElement('div');
    header.className = 'header_movie';
    
    const titleElement = document.createElement('h1');
    titleElement.innerText = jsonData.details.title;
    header.appendChild(titleElement);
    details.appendChild(header);
    
    const info = document.createElement('div');
    info.className = 'info_movie';
    info.innerHTML = `
        <div><strong> ${jsonData.details.release_date}</div>  <div><img class="star" src="static/img/star.png">${jsonData.details.vote_average} </div> <div> ${jsonData.details.runtime} min </strong> </div>
    `;
    
    details.appendChild(info);

    const summary = document.createElement('div');
    summary.className = 'summary_movie';
    summary.innerText = jsonData.details.overview;
    details.appendChild(summary);

    const extraInfo = document.createElement('div');
    extraInfo.className = 'extra-info_movie';
    extraInfo.innerHTML = `
        <div><strong></strong> ${jsonData.details.genres.map(genre => genre.name).join(', ')}</div>
        <div><strong>Budget: </strong> $${jsonData.details.budget.toLocaleString()}</div>
        <div><strong>Revenue: </strong> $${jsonData.details.revenue.toLocaleString()}</div>
    `;
    poster.appendChild(extraInfo);

    const production = document.createElement('div');
    production.className = 'production_movie';
    const productionCompanies = jsonData.details.production_companies.map(company => company.name).join(', ');
    production.innerHTML = `<p><strong>Production Companies: </strong> ${productionCompanies}</p>`;
    details.appendChild(production);


    const actors = document.createElement('div');
    actors.className = 'actors_movie';
    const actorList = jsonData.actors.map(actor => `${actor[0]}`).join(', ');
    actors.innerHTML = `<p><strong>Actors: </strong>${actorList}</p>`;
    details.appendChild(actors);

    container.appendChild(poster);
    container.appendChild(details);

    
    var lastMessage = $('.zone-messages .message').last().find('.article');
    lastMessage.append(container);
}

function createArticlePerson(jsonData) {
    const container = document.createElement('div');
    container.className = 'container_person';

    const details = document.createElement('div');
    details.className = 'details_person';

    const header = document.createElement('div');
    header.className = 'header_person';

    const titleElement = document.createElement('h1');
    titleElement.innerText = jsonData.details.name;
    header.appendChild(titleElement);
    details.appendChild(header);

    const info = document.createElement('div');
    info.className = 'info_person';
    const birthDate = new Date(jsonData.details.birthday).toLocaleDateString();
    const deathDate = jsonData.details.deathday ? new Date(jsonData.details.deathday).toLocaleDateString() : 'Still alive';
    info.innerHTML = `
        <p><strong>Date of Birth: </strong>${birthDate}</p>
        <p><strong>Date of Death: </strong>${deathDate}</p>
    `;
    details.appendChild(info);

    const biography = document.createElement('div');
    biography.className = 'biography_person';
    biography.innerHTML = `<p><strong>Biography: </strong>${jsonData.details.biography}</p>`;
    details.appendChild(biography);

    const poster = document.createElement('div');
    poster.className = 'poster_person';

    const posterImg = document.createElement('img');
    posterImg.src = `https://image.tmdb.org/t/p/w500${jsonData.details.profile_path}`;
    poster.appendChild(posterImg);
    container.appendChild(poster);

    const movies = document.createElement('div');
    movies.className = 'movies_person';
    const moviesList = jsonData.actors_series.map(movie => `${movie[0]}`).join(', ');
    movies.innerHTML = `<p><strong>Movies: </strong>${moviesList}</p>`;
    details.appendChild(movies);

    const series = document.createElement('div');
    series.className = 'series_person';
    const seriesList = jsonData.actors_tv.map(series => `${series[0]}`).join(', ');
    series.innerHTML = `<p><strong>Series: </strong>${seriesList}</p>`;
    details.appendChild(series);

    container.appendChild(details);

   
    var lastMessage = $('.zone-messages .message').last().find('.article');
    lastMessage.append(container);
}

function createArticleSeries(jsonData) {
    const container = document.createElement('div');
    container.className = 'container_series';

    const poster = document.createElement('div');
    poster.className = 'poster_series';

    const posterImg = document.createElement('img');
    posterImg.src = `https://image.tmdb.org/t/p/w500${jsonData.details.poster_path}`;
    poster.appendChild(posterImg);
    container.appendChild(poster);

    const details = document.createElement('div');
    details.className = 'details_series';

    const header = document.createElement('div');
    header.className = 'header_series';

    const titleElement = document.createElement('h1');
    titleElement.innerText = jsonData.details.name;
    header.appendChild(titleElement);
    details.appendChild(header);

    const info = document.createElement('div');
    info.className = 'info_series';
    info.innerHTML = `
        <div><strong>First Air Date: </strong>${jsonData.details.first_air_date}</div>  <div><strong>Number of Seasons: </strong>${jsonData.details.number_of_seasons}</div>
    `;

    const info2 = document.createElement('div');
    info2.className = 'info_series';
    info2.innerHTML = `<div><strong>Last Air Date: </strong>${jsonData.details.last_air_date}</div>  <div><strong>Number of Episodes: </strong>${jsonData.details.number_of_episodes}</div>`;

    details.appendChild(info);
    details.appendChild(info2);

    const overview = document.createElement('div');
    overview.className = 'overview_series';
    overview.innerHTML = `<p>${jsonData.details.overview}</p>`;
    details.appendChild(overview);

    const lastEpisodeSeparator = document.createElement('div');
    lastEpisodeSeparator.className = 'last-episode_separator';
    details.appendChild(lastEpisodeSeparator);

    const lastEpisode = jsonData.details.last_episode_to_air;
    const lastEpisodeInfo = document.createElement('div');
    lastEpisodeInfo.className = 'last-episode_series';
    const actorsList = jsonData.actors.map(actor => actor[0]).join(', ');
    lastEpisodeInfo.innerHTML = `
        <p><strong>Last Episode: </strong> ${lastEpisode.name}</p>
        <div class="runtime-rating">
            <p>${lastEpisode.runtime} min</p>
            <p><img class="star" src="static/img/star.png">${lastEpisode.vote_average}</p>
        </div>
        <p>${lastEpisode.overview}</p>
        <p><strong>Actors: </strong>${actorsList}</p>
    `;
    details.appendChild(lastEpisodeInfo);

    const genres = document.createElement('div');
    genres.className = 'genres_series';
    const genresList = jsonData.details.genres.map(genre => genre.name).join(', ');
    genres.innerHTML = `<p><strong> ${genresList} </strong></p>`;

    const createdBy = document.createElement('div');
    createdBy.className = 'created-by_series';
    const createdByList = jsonData.details.created_by.map(creator => creator.name).join(', ');
    createdBy.innerHTML = `<p><strong>Created By:</strong> ${createdByList}</p>`;

    const networks = document.createElement('div');
    networks.className = 'networks_series';
    const networkList = jsonData.details.networks.map(network => network.name).join(', ');
    networks.innerHTML = `<p><strong>Networks:</strong> ${networkList}</p>`;

    poster.appendChild(genres);
    poster.appendChild(createdBy);
    poster.appendChild(networks);

    container.appendChild(details);

    var lastMessage = $('.zone-messages .message').last().find('.article');
    lastMessage.append(container);

}

function createConversation(mode){
    numberchat++;
    numberchatactuel = numberchat;
    const zone = document.querySelector('.page2_content_history');
    const conversation = document.createElement('div');
    conversation.id = 'conversation' + numberchat;
    conversation.className = 'conversation';
    const conversationTitle = document.createElement('h1');
    conversationTitle.className = 'conversation-title';
    conversationTitle.textContent = 'New Chat - ' + mode;
    conversation.appendChild(conversationTitle);
    zone.appendChild(conversation);
    conversation.classList.add('active');

    $.ajax({
        url: '/save_conversation',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ content: "", numberchat: numberchat }),
        success: function(response) {

        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Failed to save conversation.');
        }
    });


    $.ajax({
        url: '/add_to_historique',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ name: conversation.id, title: conversationTitle.textContent }),
        success: function(response) {
            console.log(response.message);
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Failed to add to historique.');
        }
    });

    $('.conversation').click(function() {
        const conversationId = $(this).attr('id');
        document.querySelectorAll('.conversation').forEach(conversation => {
            conversation.classList.remove('active');
        });
        $(this).toggleClass('active');

        $.ajax({
            url: `/load_conversation/${conversationId}`,
            type: 'GET',
            contentType: 'application/json',
            success: function(response) {
                numberchatactuel = conversationId.match(/\d+/)[0];
                createZoneMessage(response.content);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Failed to load conversation.');
            }
        });
    });
}
function loadConversationTitles() {
    $.ajax({
        url: '/get_conversation_titles',
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            response.forEach(conversation => {
                createConversationHistorique(conversation.name, conversation.title);
            });
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
}

function createConversationHistorique(name, title){
    const zone = document.querySelector('.page2_content_history');
    const conversation = document.createElement('div');
    conversation.id = name;
    conversation.className = 'conversation';
    const conversationTitle = document.createElement('h1');
    conversationTitle.className = 'conversation-title';
    conversationTitle.textContent = title
    conversation.appendChild(conversationTitle);
    zone.appendChild(conversation);

    

    $('.conversation').click(function() {
        document.querySelectorAll('.conversation').forEach(conversation => {
            conversation.classList.remove('active');
        });
        $(this).toggleClass('active');
        const conversationId = $(this).attr('id');

        $.ajax({
            url: `/load_conversation/${conversationId}`,
            type: 'GET',
            contentType: 'application/json',
            success: function(response) {
                numberchatactuel = conversationId.match(/\d+/)[0];
                createZoneMessage(response.content);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Failed to load conversation.');
            }
        });
    });
}

function createZoneMessage(content){

    console.log(content);

    $('.page2_content_right').empty();

    const page2ContentRight = document.querySelector('.page2_content_right');
    const page2Bottom = document.querySelector('.page2_bottom');
    const imageFond = document.createElement('img');
    imageFond.src = 'static/img/logo_fond.png';
    imageFond.alt = 'Logo';
    imageFond.className = 'logoFond';
    page2ContentRight.appendChild(imageFond);
    const zoneMessages = document.createElement('div');
    zoneMessages.className = 'zone-messages';
    zoneMessages.innerHTML = content;
    page2ContentRight.appendChild(zoneMessages);

    const  buttonNewChat = document.createElement('button');
    buttonNewChat.className = 'buttonNewChat';
    buttonNewChat.textContent = 'New Chat';
    page2Bottom.appendChild(buttonNewChat);

    const topButton = document.createElement('button');
    topButton.className = 'scrollToTopButton';
    topButton.textContent = 'Top';
    page2ContentRight.appendChild(topButton);

    const jsonOutput = document.createElement('pre');
    jsonOutput.id = 'jsonOutput';
    page2ContentRight.appendChild(jsonOutput);

    var lastMessage = $('.zone-messages .message').last();
    var dataValue = lastMessage.attr('data-value');

    localStorage.setItem('mode', dataValue);
    console.log(dataValue);   // Affiche le texte du bouton dans la console (pour vérification)
    createDropdown(dataValue);
    dropdownAnim();

    $('.buttonNewChat').click(function() {            
        const content = $('.zone-messages').html();
    
        $.ajax({
            url: '/save_conversation',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ content: content, numberchat: numberchatactuel }),
            success: function(response) {
 
                changeScene(2);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Failed to save conversation.');
            }
        });


    });

    $('.scrollToTopButton').click(function() {
        scrollToTop();
    });


}



