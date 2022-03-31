const color = {
    'unrated': '#2d2d2d',
    'bronze': '#ad5600',
    'silver': '#435f7a',
    'gold': '#ec9a00',
    'platinum': '#27e2a4',
    'diamond': '#00b4fc',
    'ruby': '#ff0062',
}

const tier2color = (tier: number, verbose: boolean = false) => {
    if (verbose) {
        if (tier >= 1 && tier <= 5) {
            return 'bronze'
        } else if (tier >= 6 && tier <= 10) {
            return 'silver'
        } else if (tier >= 11 && tier <= 15) {
            return 'gold'
        } else if (tier >= 16 && tier <= 20) {
            return 'platinum'
        } else if (tier >= 21 && tier <= 25) {
            return 'diamond'
        } else if (tier >= 26 && tier <= 30) {
            return 'ruby'
        }
    } else {
        switch (tier) {
            case 1:
                return 'bronze'
            case 2:
                return 'silver'
            case 3:
                return 'gold'
            case 4:
                return 'platinum'
            case 5:
                return 'diamond'
            case 6:
                return 'ruby'
        }
    }
    return 'unrated'
}

const getColor = (tier: string) => {
    switch (tier) {
        case 'unrated':
            return color.unrated
        case 'bronze':
            return color.bronze
        case 'silver':
            return color.silver
        case 'gold':
            return color.gold
        case 'platinum':
            return color.platinum
        case 'diamond':
            return color.diamond
        case 'ruby':
            return color.ruby
    }
    return "undefined"
}

export default color
export { tier2color, getColor }
