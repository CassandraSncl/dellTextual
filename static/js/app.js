let previousScene = 2;

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


    // Ajout du titre de l'application
    const appLogo = document.createElement('img');
    appLogo.src = 'static/img/logo.png';
    appLogo.alt = 'AI Logo';
    appLogo.className = 'appLogo';
    // gsap.from(appName, {duration: 1, x:-100,opacity: 0, ease: 'back.out(1.7)'});
    page2Header.appendChild(appLogo);

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

    page2Bottom.appendChild(chatText);
    containerPage2.appendChild(page2Bottom);

    // Ajout du conteneur principal à la page
    document.body.appendChild(containerPage2);  



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

        $('.buttonNewChat').click(function() {            
            // fetch('data/conversation/conv.json')            
            // .then(response => response.json())
            // .then(data => {
            //     // Parcours les messages du fichier JSON
            //     data.conversation.forEach(message => {
            //         // Vérifie l'auteur du message
            //         if (message.auteur === 'humain') {
            //             // Affiche le message comme venant de l'humain
            //             addMessageHuman(message.message);
            //         } else if (message.auteur === 'bot') {
            //             // Affiche le message comme venant du bot
            //             addMessageBot(message.message);
            //         }
            //     });
            // })
            // .catch(error => {
            //     console.error('Erreur lors du chargement du fichier JSON :', error);
            // });
            const messages = stringify("data/conversation/conv.json");
            console.log(messages);
        });

        $('.scrollToTopButton').click(function() {
            scrollToTop();
        });

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
    const assistantChoice = document.createElement('img');
    assistantChoice.src = 'static/img/assistant.png';
    assistantChoice.alt = 'assistant Choice';
    assistantChoice.className = 'assistantChoice';
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
    container.appendChild(assistantChoice);
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
        addMessageHuman(message);
        $('.chatInput').val('');
        addMessageBot("Le Lorem Ipsum est simplement du faux texte employé dans la composition et la mise en page avant impression. Le Lorem Ipsum est le faux texte standard de l'imprimerie depuis les années 1500, quand un imprimeur anonyme assembla ensemble des morceaux de texte pour réaliser un livre spécimen de polices de texte. Il n'a pas fait que survivre cinq siècles, mais s'est aussi adapté à la bureautique informatique, sans que son contenu n'en soit modifié. Il a été popularisé dans les années 1960 grâce à la vente de feuilles Letraset contenant des passages du Lorem Ipsum, et, plus récemment, par son inclusion dans des applications de mise en page de texte, comme Aldus PageMaker.");
    }
}

function addMessageHuman(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
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

function addMessageBot(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    const messageBot = document.createElement('div');
    messageBot.className = 'bot-message';

    const messageText = document.createElement('p');
    messageText.className = 'bot-message-text';
    messageText.textContent = message;

    messageBot.appendChild(messageText);
    messageDiv.appendChild(messageBot);

    $('.zone-messages').append(messageDiv);

    scrollToBottom();
}


