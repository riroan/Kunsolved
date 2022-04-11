import React from 'react'
import styles from './header.module.scss'
import { Link } from 'react-router-dom'
import classnames from 'classnames/bind'
const cx = classnames.bind(styles)

export default function Header() {
    return (
        <div className={cx('main')}>
            <Link to="/" className={cx('link')}>
                <span className={cx('title')}>SchoolJoon</span>
            </Link>
            <div className={cx('ext')}>
                <ul className={cx('ul')}>
                    <li className={cx('list')}>
                        <a className={cx('a', 'ex')} href="https://www.acmicpc.net/school/ranklist/194">
                            백준
                        </a>
                    </li>
                    <li className={cx('list')}>
                        <a className={cx('a', 'ex')} href="https://solved.ac/ranking/o/194">
                            solved
                        </a>
                    </li>
                    <li className={cx('list')}>
                        <Link to="/issue" className={cx('a')}>
                            기능요청
                        </Link>
                    </li>
                </ul>
            </div>
        </div>
    )
}
