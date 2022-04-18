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
import { problemType } from '../../_config/types'
import Sort, { SortType } from '../../sort'
const cx = classnames.bind(styles)

export default function DetailPage() {
    const { level } = useParams()
    const [data, setData] = useState<problemType[]>([])
    const [elements, setElements] = useState<ReactElement[]>([])
    const updateElement = () => {
        const title = [
            <li key={-1} className={cx('list', 'title')}>
                <span className={cx('name')}>문제 번호</span>
                <span className={cx('value')}>문제</span>
            </li>,
        ]
        if (data.length > 0) {
            setElements(
                title.concat(
                    data.map((value: problemType, ix: number) => (
                        <a href={`https://www.acmicpc.net/problem/${value.id}`} className={cx('a')}>
                            <li key={ix} className={cx('list')}>
                                <span className={cx('name')}>{value.id}</span>
                                <span className={cx('value')}>{value.title}</span>
                            </li>
                        </a>
                    ))
                )
            )
        } else {
            setElements(title.concat(<li className={cx('all')}>안 푼 문제가 없습니다!</li>))
        }
    }
    useEffect(() => {
        var url = `${URL}/v1/unsolved/level?level=${level}`
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                setData(res)
            })
    }, [level])
    useEffect(() => {
        updateElement()
    }, [data])
    return (
        <div>
            <Header />
            <Menu />
            <div className={cx('header')} style={{ color: color[tier2color(parseInt(level ? level : '0'), true)] }}>
                <img src={`https://static.solved.ac/tier_small/${level}.svg`} alt={level} className={cx('image')} />
                {level2tier(parseInt(level ? level : '0'))}
            </div>
            <Sort
                sortFunction={(flag, type) => {
                    if (type === SortType.RANDOM) {
                        setData(data.sort(() => Math.random() - 0.5))
                    } else if (flag) {
                        setData(data.reverse())
                    } else {
                        let cmp
                        switch (type) {
                            case SortType.ID:
                                cmp = (a: problemType, b: problemType) => {
                                    if (a.id > b.id) return 1
                                    else if (a.id < b.id) return -1
                                    return 0
                                }
                                break
                            case SortType.LEVEL:
                                cmp = (a: problemType, b: problemType) => {
                                    if (a.tier > b.tier) return 1
                                    else if (a.tier < b.tier) return -1
                                    if (a.id > b.id) return 1
                                    else if (a.id < b.id) return -1
                                    return 0
                                }
                                break
                            case SortType.TITLE:
                                cmp = (a: problemType, b: problemType) => {
                                    if (a.title > b.title) return 1
                                    else if (a.title < b.title) return -1
                                    return 0
                                }
                                break
                        }
                        setData(data.sort(cmp))
                    }
                    updateElement()
                }}
            />
            <ItemSet data={elements} />
        </div>
    )
}
