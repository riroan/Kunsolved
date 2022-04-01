const level2tier = (level: number) => {
    switch (level) {
        case 0:
            return 'Unrated'
        case 1:
            return 'Bronze 5'
        case 2:
            return 'Bronze 4'
        case 3:
            return 'Bronze 3'
        case 4:
            return 'Bronze 2'
        case 5:
            return 'Bronze 1'
        case 6:
            return 'Silver 5'
        case 7:
            return 'Silver 4'
        case 8:
            return 'Silver 3'
        case 9:
            return 'Silver 2'
        case 10:
            return 'Silver 1'
        case 11:
            return 'Gold 5'
        case 12:
            return 'Gold 4'
        case 13:
            return 'Gold 3'
        case 14:
            return 'Gold 2'
        case 15:
            return 'Gold 1'
        case 16:
            return 'Platinum 5'
        case 17:
            return 'Platinum 4'
        case 18:
            return 'Platinum 3'
        case 19:
            return 'Platinum 2'
        case 20:
            return 'Platinum 1'
        case 21:
            return 'Diamond 5'
        case 22:
            return 'Diamond 4'
        case 23:
            return 'Diamond 3'
        case 24:
            return 'Diamond 2'
        case 25:
            return 'Diamond 1'
        case 26:
            return 'Ruby 5'
        case 27:
            return 'Ruby 4'
        case 28:
            return 'Ruby 3'
        case 29:
            return 'Ruby 2'
        case 30:
            return 'Ruby 1'
    }
    return 'Unrated'
}

export default level2tier
