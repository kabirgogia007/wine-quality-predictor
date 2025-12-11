
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, AlertCircle, Wine } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Prediction() {
    const [features, setFeatures] = useState([]);
    const [formData, setFormData] = useState({});
    const [loading, setLoading] = useState(true);
    const [predicting, setPredicting] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchFeatures();
    }, []);

    const fetchFeatures = async () => {
        try {
            const res = await axios.get(`${API_URL}/features`);
            const featList = res.data.features || [];
            setFeatures(featList);

            // Initialize form defaults
            const initialData = {};
            featList.forEach(f => initialData[f] = 0);
            setFormData(initialData);

            if (featList.length === 0) setError("No features found. Setup backend first.");
        } catch (err) {
            console.error(err);
            setError("Failed to connect to backend. Ensure server is running.");
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || 0 });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setPredicting(true);
        setResult(null);
        try {
            const res = await axios.post(`${API_URL}/predict`, { features: formData });
            setResult(res.data);
        } catch (err) {
            console.error(err);
            setError("Prediction failed. " + (err.response?.data?.detail || err.message));
        } finally {
            setPredicting(false);
        }
    };

    if (loading) return <div className="flex justify-center p-20"><Loader2 className="animate-spin text-gold w-10 h-10" /></div>;
    if (error && !features.length) return <div className="text-red-400 text-center p-20"><AlertCircle className="inline mb-1 mr-2" />{error}</div>;

    return (
        <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Input Section */}
            <div className="lg:col-span-2 space-y-6">
                <h2 className="text-3xl mb-4">Wine Properties</h2>
                <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-dark-card p-6 rounded-lg border border-gray-800">
                    {features.map((feature) => (
                        <div key={feature} className="space-y-1">
                            <label className="text-sm text-gray-400 uppercase tracking-wider text-xs">
                                {feature.replace(/_/g, ' ')}
                            </label>
                            <input
                                type="number"
                                step="0.01"
                                name={feature}
                                value={formData[feature]}
                                onChange={handleChange}
                                className="input-field"
                                required
                            />
                        </div>
                    ))}
                    <div className="md:col-span-2 pt-4">
                        <button
                            type="submit"
                            disabled={predicting}
                            className="w-full btn-primary flex justify-center items-center py-3 text-lg"
                        >
                            {predicting ? <Loader2 className="animate-spin mr-2" /> : "Assess Quality"}
                        </button>
                    </div>
                </form>
            </div>

            {/* Result Section */}
            <div className="lg:col-span-1">
                <h2 className="text-3xl mb-4">Verdict</h2>
                <AnimatePresence mode='wait'>
                    {result ? (
                        <motion.div
                            key="result"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="bg-dark-card p-6 rounded-xl border-l-4 border-gold shadow-2xl space-y-4 sticky top-24"
                        >
                            <div className="text-center pb-4 border-b border-gray-700">
                                <span className="text-sm text-gray-500 uppercase">Estimated Score</span>
                                <div className="text-6xl font-serif text-gold my-2">{result.score} <span className="text-2xl text-gray-600">/ 10</span></div>
                                <div className={`text-xl font-bold ${result.score >= 7 ? 'text-green-400' : result.score >= 5 ? 'text-yellow-400' : 'text-red-400'}`}>
                                    {result.verdict}
                                </div>
                            </div>
                            <div className="pt-2">
                                <h4 className="text-gold mb-2 text-sm uppercase font-bold">Sommelier Notes</h4>
                                <p className="text-gray-300 italic text-sm leading-relaxed">"{result.advice}"</p>
                            </div>
                        </motion.div>
                    ) : (
                        <div className="bg-dark-card/50 p-8 rounded-xl border border-dashed border-gray-700 text-center text-gray-500 h-64 flex flex-col items-center justify-center">
                            <Wine className="w-12 h-12 mb-4 opacity-20" />
                            <p>Submit wine properties to receive an assessment.</p>
                        </div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
