// src/app/components/PriceCard.tsx
'use client';
import React from 'react';
import clientLogger from '@/lib/clientLogger';

interface PriceCardProps {
  priceId: string;
  name: string;
  amount: number;
  image: string;
  onSelect: (priceId: string) => void;
}

export default function PriceCard({ image, name, priceId, amount, onSelect }: PriceCardProps) {
  const handleSelectClick = (priceId: string) => {
    clientLogger.info(`Selected plan: ${name}, Price ID: ${priceId}`);
    onSelect(priceId); // 実際のonSelect関数を呼び出す
  };

  return (
    <div className='bg-white rounded-lg shadow-md p-5 m-1 w-full max-w-sm text-gray-600'>
      <img
        src={image}
        alt={`${name} プラン`}
        className='mb-4 w-full'
        style={{ height: '150px', objectFit: 'cover' }}
      />
      <h2 className='text-xl font-semibold mb-4 text-center'>{name}</h2>
      <h3 className='text-center mb-12 text-black'>
        Price: <span className='text-2xl font-bold text-black'>¥{amount}</span>
      </h3>
      <div className='flex justify-center'>
        <button
          onClick={() => handleSelectClick(priceId)}
          className='bg-[#66b2ff] text-black py-2 px-4 rounded-full hover:bg-[#99ccff] focus:outline-non active:transform active:translate-y-1  '
        >
          Select
        </button>
      </div>
    </div>
  );
}
