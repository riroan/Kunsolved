import React, { useEffect, useState, ReactElement } from 'react'
import Menu from '../../menu'
import Header from '../../header'
import ItemSet from '../../itemset'
import styles from './TagPage.module.scss'
import classnames from 'classnames/bind'
import { Link } from 'react-router-dom'
import color, { tier2color } from '../../_config/color'
import URL from '../../_config/config'
const cx = classnames.bind(styles)

export default function TagPage() {
    const [data, setData] = useState<ReactElement[]>([])
    useEffect(() => {
        var url = `${URL}/statusByTag`
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
                        <span className={cx('name')}>알고리즘 태그</span>
                        <span className={cx('value')}>해결한 문제 / 전체 문제</span>
                    </li>,
                ]
                for (var i in res) tmp.push({ name: i, ...res[i] })
                setData(
                    title.concat(
                        tmp.map((value, ix) => (
                            <li key={ix} className={cx('list')}>
                                <span className={cx('name')}>
                                    <Link to={`/tag/${value.name}`} className={cx('link')} style={{ color: color[tier2color(value.level, true)] }}>
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
            <ItemSet data={data} />
        </div>
    )
}
