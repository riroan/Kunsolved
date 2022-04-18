import React, { useEffect, useState, ReactElement } from 'react'
import Menu from '../../menu'
import Header from '../../header'
import ItemSet from '../../itemset'
import styles from './TierPage.module.scss'
import classnames from 'classnames/bind'
import { Link } from 'react-router-dom'
import color, { tier2color } from '../../_config/color'
import URL from '../../_config/config'
const cx = classnames.bind(styles)

export default function TierPage() {
    const [data, setData] = useState<ReactElement[]>([])
    useEffect(() => {
        var url = `${URL}/v1/status/level`
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                var tmp = []
                const title = [
                    <li key={-1} className={cx('list', 'title')}>
                        <span className={cx('name')}>레벨</span>
                        <span className={cx('value')}>해결한 문제 / 전체 문제</span>
                    </li>,
                ]
                for (var i in res) {
                    tmp.push({ level: parseInt(i), ...res[i] })
                }
                setData(
                    title.concat(
                        tmp.map((value, ix) => (
                            <li key={ix} className={cx('list')}>
                                <span className={cx('name')}>
                                    <img className={cx('image')} src={`https://static.solved.ac/tier_small/${value.level}.svg`} alt={value.name} />
                                    <Link to={`/tier/${value.level}`} className={cx('link')} style={{ color: color[tier2color(value.level, true)] }}>
                                        {value.name}
                                    </Link>
                                </span>
                                <span className={cx('value')}>
                                    {value.solved_cnt} / {value.all_cnt}
                                </span>
                            </li>
                        ))
                    )
                )
            })
    }, [])
    return (
        <div>
            <Header />
            <Menu />
            <ItemSet data={data} usePagination={false} />
        </div>
    )
}
