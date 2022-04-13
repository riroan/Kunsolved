import React, { useEffect, useState } from 'react'
import Menu from '../../menu'
import Header from '../../header'
import styles from './TierPage.module.scss'
import classnames from 'classnames/bind'
import { Link } from 'react-router-dom'
import color, { tier2color } from '../../_config/color'
import URL from '../../_config/config'
const cx = classnames.bind(styles)

export default function TierPage() {
    const [tierTable, setTierTable] = useState<Array<Array<Tier>>>([])
    interface Tier{
        level: number,
        solved_cnt: number,
        all_cnt: number
        name: string
    }

    useEffect(() => {
        var url = `${URL}/statusByLevel`
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                var table = []
                for(var tier = 0; tier < 6; tier++) {
                    var tmp: Array<Tier> = []
                    for (var tierDetail = 1; tierDetail <= 5; tierDetail++) {
                        tmp.push({level: tier * 5 + tierDetail, ...res[tier * 5 + tierDetail]});
                    }
                    table.push(tmp);
                }
                table.push([{level: 0, ...res[0]}]);
                setTierTable(table);
            })

    }, [])
    return (
        <div>
            <Header />
            <Menu />
            <div className={cx('tier-wrapper')}>
                {
                    tierTable.map((row, ix) =>(
                        <div className={cx('tier-row')}>
                            {
                                row.map((tier, ixx) =>(
                                    <div className={cx('tier-level')}>
                                        <Link to={`/tier/${tier.level}`} className={cx('link')} style={{ color: color[tier2color(tier.level, true)] }} >
                                            <img className={cx('image')} src={`https://static.solved.ac/tier_small/${tier.level}.svg`} alt={tier.name} />

                                        </Link>
                                        <div className={cx('tier-details')} style={{ color: color[tier2color(tier.level, true)] }}>
                                            {tier.solved_cnt} / {tier.all_cnt}
                                        </div>
                                    </div>
                                ))
                            }
                        </div>
                    ))
                }
            </div>
        </div>
    )
}
