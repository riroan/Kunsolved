import React, { useEffect, useState, ReactElement } from 'react'
import { useParams } from 'react-router-dom'
import Header from '../../header'
import Menu from '../../menu'
import ItemSet from '../../itemset'
import styles from './TagDetailPage.module.scss'
import classnames from 'classnames/bind'
import { problemType } from '../../_config/types'
import Sort, { SortType } from '../../sort'
import URL from '../../_config/config'
const cx = classnames.bind(styles)

export default function TagDetailPage() {
    const { name } = useParams()
    const [data, setData] = useState<problemType[]>([])
    const [elements, setElements] = useState<ReactElement[]>([])
    const [check, setCheck] = useState<boolean>(false)
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
                        <a key={ix} href={`https://www.acmicpc.net/problem/${value.id}`} className={cx('a')}>
                            <li className={cx('list')}>
                                <span className={cx('name')}>
                                    {!check && <img className={cx('image')} src={`https://static.solved.ac/tier_small/${value.tier}.svg`} alt={value.title} />}
                                    <div className={cx('id')}>{value.id}</div>
                                </span>
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
        var url = `${URL}/v1/unsolved/tag?name=${name}`
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
    }, [name])
    useEffect(() => {
        updateElement()
    }, [data, check])
    return (
        <div>
            <Header />
            <Menu />
            <div className={cx('header', 'common')}>{name}</div>
            <Sort
                hide={true}
                handleChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setCheck(event.target.checked)
                }}
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
                            case SortType.NUM_SOLVED:
                                cmp = (a: problemType, b: problemType) => {
                                    if (a.num_solved > b.num_solved) return 1
                                    else if (a.num_solved < b.num_solved) return -1
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
