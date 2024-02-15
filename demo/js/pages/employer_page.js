$(document).ready(() => {
    /**
     * Mockup data for employer
     * */
    let emp1 = new Employer('Antonino', 'Lorenzo', 'anton@gmail.com', 'S3cur3P@ssword', 'Turing Careers')
    let emp2 = new Employer('John', 'Doe', 'john.doe@gmail.com', 'S3cur3P@ssword', 'E-Corp')

    let offer1 = new Offer(
        'Data Engineer',
        'Placeholder Description',
        emp1,
        [
            new Skill(1, 'Python', 'Programming Language'),
            new Skill(3, 'PostgreSQL', 'Database'),
            new Skill(5, 'Pandas', 'Framework'),
            new Skill(6, 'TensorFlow', 'Framework')
        ],
        'Remote',
        new Location('Milano, Italia'),
        [new Languages('Italiano')]
    )

    let offer2 = new Offer(
        'Data Scientist',
        'Placeholder Description',
        emp1,
        [
            new Skill(1, 'Python', 'Programming Language'),
            new Skill(2, 'C++', 'Programming Language'),
            new Skill(3, 'PostgreSQL', 'Database'),
            new Skill(7, 'Scikit Learn', 'Framework'),
            new Skill(4, 'Pandas', 'Framework'),
            new Skill(8, 'TensorFlow', 'Framework'),
            new Skill(9, 'PyTorch', 'Framework')
        ],
        'OnSite',
        new Location('Milano, Italia'),
        [new Languages('Italiano')]
    )

    let offer3 = new Offer(
        'Frontend Developer',
        'Placeholder Description',
        emp2,
        [
            new Skill(10, 'Javascript', 'Programming Language'),
            new Skill(11, 'React', 'Framework'),
            new Skill(12, 'Node .js', 'Framework'),
            new Skill(13, 'CSS', 'Programming Language'),
            new Skill(10, 'Typescript', 'Programming Language'),
        ],
        'Remote',
        new Location('Milano, Italia'),
        [new Languages('Italiano')]
    )

    let offer4 = new Offer(
        'Backend Developer',
        'Placeholder Description',
        emp2,
        [
            new Skill(14, 'Java', 'Programming Language'),
            new Skill(16, 'MySQL', 'Database'),
            new Skill(17, 'Spring', 'Framework'),
            new Skill(18, 'Google Cloud', 'Cloud'),
            new Skill(19, 'Kafka', 'Framework'),
        ],
        'OnSite',
        new Location('Milano, Italia'),
        [new Languages('Italiano')]
    )

    const firstEmployerOffers = [offer1, offer2]
    const secondEmployerOffers = [offer3, offer4]


    /**
     * Offer Form
     * */
    const createOfferButton = $("#create-offer-button")
    const offerForm = $("#create-offer-form-wrapper")
    createOfferButton.click(() => {
        offerForm.removeClass('display-none')
    })

    const undoButton = $("#offer-form-undo-button")
    const submitButton = $("#offer-form-submit-button")

    undoButton.click(() => {
        // TODO: clean up offer form
        // TODO: notify user
        offerForm.addClass('display-none')
    })

    submitButton.click(() => {
        // Make POST request to create offer
        $.ajax({
            url: 'http://localhost:8080/TuringCareers_war/offers',
            method: 'POST',
            data: { offer: getOfferForm() },
            dataType: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error:', textStatus, errorThrown);
            }
        });
    })

    function getOfferForm() {
        const titleInput = $("#offer-title")
        const descriptionInput = $("#offer-description")
        const locationInput = $("#locations-input-text")
        const skillTags = $("#skill-tags .skill-tag")
        const languagesTags = $("#language-tags")

        let title = titleInput.val()
        let description = descriptionInput.val()
        let locType = 'IN_PLACE'
        let location = locationInput.val()

        let skills = []
        skillTags.each(function() {
            let skillText = $(this).find('p').text().trim();
            skills.push(skillText);
        });
        let languages = []
        languagesTags.each(function() {
            let languageText = $(this).find('p').text().trim();
            languages.push(languageText);
        });

        let offer = new Offer(title, description, skills, locType, location, languages)
        console.log(JSON.stringify(offer))
        return offer;
    }


    /**
     * Developer Recommendation
     * */

    function getRecommendedDevelopers(showDevelopers, offer, listWrapper) {
        if ($(showDevelopers).prop('checked')) {
            listWrapper.removeClass('display-none');
            recommendDevelopers(offer, listWrapper)
        } else {
            $(".of-offer-matching-developers").addClass('display-none');
        }
    }

    /**
     * Extracts a list of Developers from a JSON response
     * @param response
     * */
    function extractDeveloper(response) {
        let out = []
        for (let item of response) {
            out.push(new Developer(
                item['_Developer__id'],
                item['_Developer__f_name'] ? item['_Developer__f_name'] : '',
                item['_Developer__l_name'] ? item['_Developer__l_name'] : '',
                item['_Developer__bio'],
                item['_Developer__location'] ? item['_Developer__location']: '',
                '',
                item['_Developer__location'] ? item['_Developer__location'] : '',
                item['_Developer__skills'],
                item['_Developer__languages'] ? item['_Developer__languages'] : ''
            ))
        }
        return out
    }

    /**
     *
     * @param items a list of developers developers
     * @param wrapper the offer associated with the developers
     * */
    function updateOfferList(items, wrapper) {
        if (items.length == 0) {
            let card = $("<div>")
                .addClass('item-card')
                .append($("<h3>")
                    .addClass('no-select inter-light')
                    .text('No Results Found')
                )
            wrapper.append(card)
        }
        let i = 0
        for (let item of items) {
            if (i < 3) {
                let card = $("<div>")
                    .addClass('item-card')

                let generals = $("<div>")
                    .addClass('dev-generals')
                let locations = $("<h3>")
                    .addClass('dev-location inter-medium')
                    .text(item.loc ? item.loc : '')
                let name = $("<h2>")
                    .addClass('dev-name inter-bold no-select')
                    .text(item.firstName + ' ' + item.lastName)
                generals.append(locations, name)


                let skills = $("<ul>")
                    .addClass('dev-skills')

                let j = 0
                for (skill of item.skills) {
                    if (j <= 3) {
                        let name = $("<li>")
                            .addClass('inter-light no-select')
                            .text(skill['_Skill__name'])
                        skills.append(name)
                        j += 1
                    }
                    else
                        break
                }
                skills.append($("<li>").addClass('inter-ligth no-select').text('...'))

                let content = $("<div>")
                    .addClass('dev-content')

                let descWrapper = $("<div>")
                    .addClass('dev-desc-preview"')
                let desc = $("<p>")
                    .addClass('inter-light no-select')
                    .text(item.bio.slice(0, 40) + '...')
                descWrapper.append(desc)

                let buttonWrapper = $("<div>")
                    .addClass('dev-details-button')
                let btnWrap = $("<div>")
                    .addClass('flex-center')
                let button = $("<a>")
                    .addClass('inter-bold no-select')
                    .text('Dettagli')
                btnWrap.append(button)
                buttonWrapper.append(btnWrap)

                content.append(descWrapper, buttonWrapper)

                card.append(generals, skills, content)
                wrapper.append(card)
                i += 1
            }
            else
                break
        }
    }

    /**
     * Called when Employer asks for recommendation on a specific offer
     * @param offer the offer that must be matched with a list of developers
     * */
    function recommendDevelopers(offer, listWrapper) {
        return $.ajax({
            url: 'http://localhost:8000/engine/v1/developers',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(offer),
            dataType: 'json',
            success: function(response) {
                devs = extractDeveloper(response)
                updateOfferList(devs, listWrapper)
            },
            error: function(jqXHR, textStatus, errorThrown) {

            }
        });
    }

    function addEmployerOffer(offer, wrapper) {
        let card = $("<div>")
            .addClass('item-card fade-in')

        let cardHeaderWrapper = $("<div>")
            .addClass('of-offer-card-header')

        let cardHeader = $("<div>")
            .addClass('of-offer-head no-select')
        let headEmployer = $("<h3>")
            .addClass('of-offer-employer-name inter-medium')
            .text(offer.employer.firstName + ' ' + offer.employer.lastName)
        let headTitle = $("<h2>")
            .addClass('of-offer-tile inter-bold no-select')
            .text(offer.title)
        cardHeader.append(headEmployer, headTitle)

        let developersListWrapper = $("<div>")
            .addClass('of-offer-matching-developers display-none')
        let developerListHeader = $("<h2>")
            .addClass('inter-bold no-select')
            .text('Matching Developers')
        let developerList = $("<div>")
            .addClass('offer-matching-developers-list')
        developersListWrapper.append(developerListHeader, developerList)

        let recommendDevelopersWrap = $("<div>")
            .addClass('show-developers-wrap')
        let recommendDevelopersIcon = $("<p>")
            .addClass('show-dev-button inter-bold')
            .text('+')
        let recommendDevelopersCheckbox = $("<input>")
            .attr('type', 'checkbox')
            .addClass('show-dev-checkbox')
            .on('change', function() {
                getRecommendedDevelopers(this, offer, developersListWrapper)
            })
        recommendDevelopersWrap.append(recommendDevelopersIcon, recommendDevelopersCheckbox)

        cardHeaderWrapper.append(cardHeader, recommendDevelopersWrap)

        let offerMeta = $("<div>")
            .addClass('of-offer-card-meta inter-regular no-select')
        let offerLocation = $("<h3>")
            .text(offer.locType === 'OnSite' ? offer.location.name: offer.locType)
        offerMeta.append(offerLocation)


        let offerContentWrapper = $("<div>")
            .addClass('of-offer-card-content')

        let offerDescPreview = $("<div>")
            .addClass('of-offer-desc-preview')
        let offerDesc = $("<p>")
            .addClass('inter-light no-select')
            .text(offer.description.slice(0, 40) + '...')
        offerDescPreview.append(offerDesc)

        let offerButtonWrapper = $("<div>")
            .addClass('of-offer-button')
        let offerButtonDiv = $("<div>")
            .addClass('flex-center')
        let offerButton = $("<a>")
            .addClass('inter-bold no-select')
            .text('Dettagli')
        offerButtonDiv.append(offerButton)
        offerButtonWrapper.append(offerButtonDiv)
        offerContentWrapper.append(offerDescPreview, offerButtonWrapper)


        card.append(cardHeaderWrapper, offerMeta, offerContentWrapper, developersListWrapper)
        wrapper.append(card)
    }

    /**
     * Corresponds to createOfferCard in search_page.js, loads the Employer offers
     * given an Offers list, in real system this is more complex and require an endpoint
     * @param items a list of offers
     * */
    function showEmployerOffer(items) {
        if (items.length > 0) {
            $("#empty-offer-list").addClass('display-none')
            for (let offer of items) {
                addEmployerOffer(offer, $("#emp-offers-list"))
            }
        }
    }


    showEmployerOffer(secondEmployerOffers)
});