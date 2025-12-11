
import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Wine, Activity, FileText, Home } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Layout() {
    const location = useLocation();

    const navItems = [
        { path: '/', label: 'Home', icon: Home },
        { path: '/predict', label: 'Predict Quality', icon: Wine },
        { path: '/dashboard', label: 'Dashboard', icon: Activity },
        { path: '/report', label: 'Report', icon: FileText },
    ];

    return (
        <div className="min-h-screen flex flex-col bg-dark-bg text-gray-100">
            <nav className="bg-dark-card border-b border-burgundy/30 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <Link to="/" className="flex items-center gap-2 group">
                            <Wine className="w-8 h-8 text-burgundy group-hover:text-gold transition-colors" />
                            <span className="text-xl font-serif font-bold text-gray-100 tracking-wide">
                                Vino<span className="text-gold">Veritas</span>
                            </span>
                        </Link>

                        <div className="flex space-x-1">
                            {navItems.map((item) => {
                                const isActive = location.pathname === item.path;
                                return (
                                    <Link
                                        key={item.path}
                                        to={item.path}
                                        className={`relative px-4 py-2 rounded-md flex items-center gap-2 text-sm font-medium transition-colors ${isActive ? 'text-gold' : 'text-gray-400 hover:text-gray-100'
                                            }`}
                                    >
                                        <item.icon className="w-4 h-4" />
                                        {item.label}
                                        {isActive && (
                                            <motion.div
                                                layoutId="underline"
                                                className="absolute bottom-0 left-0 right-0 h-0.5 bg-gold"
                                            />
                                        )}
                                    </Link>
                                );
                            })}
                        </div>
                    </div>
                </div>
            </nav>

            <main className="flex-grow max-w-7xl w-full mx-auto px-4 py-8 sm:px-6 lg:px-8">
                <Outlet />
            </main>

            <footer className="bg-dark-card border-t border-gray-800 py-6 mt-8">
                <div className="text-center text-gray-500 text-sm">
                    &copy; {new Date().getFullYear()} VinoVeritas. Artificial Intelligence by Kabir Gogia
                </div>
            </footer>
        </div>
    );
}
