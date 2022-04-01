import React, { useEffect, useState, ReactElement } from 'react'
import { useParams } from 'react-router-dom'
import Header from '../../header'
import Menu from '../../menu'
import ItemSet from '../../itemset'
import styles from './TagDetailPage.module.scss'
import classnames from 'classnames/bind'
import URL from '../../_config/config'
const cx = classnames.bind(styles)

export default function TagDetailPage() {
    const { name } = useParams()
    const [data, setData] = useState<ReactElement[]>([])
    useEffect(() => {
        var url = `${URL}/unsolvedByTag?name=${name}`
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
                    tmp.push({ id: i, ...res[i] })
                }
                if (tmp.length > 0) {
                    setData(
                        title.concat(
                            tmp.map((value, ix) => (
                                <a key={ix} href={`https://www.acmicpc.net/problem/${value.id}`} className={cx('a')}>
                                    <li className={cx('list')}>
                                        <span className={cx('name')}>
                                            <img className={cx('image')} src={`https://static.solved.ac/tier_small/${value.tier}.svg`} alt={value.name} />
                                            {value.id}
                                        </span>
                                        <span className={cx('value')}>{value.title}</span>
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
            <div className={cx('header')}>{name}</div>
            <ItemSet data={data} />
        </div>
    )
}
