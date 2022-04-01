import React, { useEffect, useState, ReactElement } from 'react'
import { useParams } from 'react-router-dom'
import Header from '../../header'
import Menu from '../../menu'
import ItemSet from '../../itemset'
import styles from './DetailPage.module.scss'
import classnames from 'classnames/bind'
import level2tier from '../../_config/tier'
import color, { tier2color } from '../../_config/color'
import URL from '../../_config/config'
const cx = classnames.bind(styles)

export default function DetailPage() {
    const { level } = useParams()
    const [data, setData] = useState<ReactElement[]>([])
    useEffect(() => {
        var url = `${URL}/unsolvedByLevel?level=${level}`
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
                        <span className={cx('name')}>문제 번호</span>
                        <span className={cx('value')}>문제</span>
                    </li>,
                ]
                for (var i in res) {
                    tmp.push({ id: i, name: res[i] })
                }
                if (tmp.length > 0) {
                    setData(
                        title.concat(
                            tmp.map((value, ix) => (
                                <a href={`https://www.acmicpc.net/problem/${value.id}`} className={cx('a')}>
                                    <li key={ix} className={cx('list')}>
                                        <span className={cx('name')}>{value.id}</span>
                                        <span className={cx('value')}>{value.name}</span>
                                    </li>
                                </a>
                            ))
                        )
                    )
                } else {
                    setData(title.concat(<li className={cx('all')}>안 푼 문제가 없습니다!</li>))
                }
            })
    }, [])
    return (
        <div>
            <Header />
            <Menu />
            <div className={cx('header')} style={{ color: color[tier2color(parseInt(level ? level : '0'), true)] }}>
                <img src={`https://static.solved.ac/tier_small/${level}.svg`} alt={level} className={cx('image')} />
                {level2tier(parseInt(level ? level : '0'))}
            </div>
            <ItemSet data={data} />
        </div>
    )
}
