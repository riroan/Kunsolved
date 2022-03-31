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
                        <a href="https://www.acmicpc.net/">백준</a>
                    </li>
                    <li className={cx('list')}>
                        <a href="https://solved.ac/">solved</a>
                    </li>
                </ul>
            </div>
        </div>
    )
}
