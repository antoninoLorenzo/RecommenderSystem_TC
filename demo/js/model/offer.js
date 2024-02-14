class Offer {
    constructor(title, description, employer, skills, locType, location, languages) {
        this.title = title;
        this.description = description;
        this.employer = employer;
        this.skills = skills;
        this.languages = languages;
        this.locType = locType;
        if (locType === 'OnSite')
            this.location = location;
        else
            this.location = undefined;
    }

    validate() {
        // TODO: implement client side validation of offers
        return true;
    }

    toJSON() {
        return {
            _Offer__title: this.title,
            _Offer__description: this.description,
            _Offer__state: 'ACTIVE',
            _Offer__location_type: this.locType,
            _Offer__location: this.location,
            _Offer__employer: this.employer,
            _Offer__languages: this.languages,
            _Offer__skills: this.skills,
        };
    }

}