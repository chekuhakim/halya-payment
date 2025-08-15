# Halya Payment System Frontend

A React application for browsing and viewing payment history for Halya residents.

## Features

- **Alley Selection**: Choose from available alleys (A, B, C, etc.)
- **House Selection**: View all houses in the selected alley
- **Payment History**: See detailed payment history for each resident
- **Payment Summary**: View total amounts, payment counts, and averages
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **React 18** with Vite
- **Supabase** for backend database
- **Tailwind CSS** for styling
- **Lucide React** for icons

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Supabase project with the Halya payment data imported

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd halya-payment-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure Supabase**
   
   Update the Supabase configuration in `src/lib/supabase.js`:
   ```javascript
   const supabaseUrl = 'YOUR_SUPABASE_URL'
   const supabaseAnonKey = 'YOUR_SUPABASE_ANON_KEY'
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:5173`

## Database Schema

The application expects the following Supabase tables:

### `residents` table
- `resident_id` (VARCHAR, Primary Key) - Format: "A001", "B023"
- `alley` (VARCHAR) - Alley letter
- `house_number` (INTEGER) - House number
- `resident_name` (VARCHAR) - Resident's full name
- `sheet_name` (VARCHAR) - Source Excel sheet

### `payments` table
- `id` (SERIAL, Primary Key)
- `resident_id` (VARCHAR, Foreign Key) - References residents.resident_id
- `payment_date` (DATE) - Payment date (nullable)
- `description` (VARCHAR) - Payment type description
- `amount` (DECIMAL) - Payment amount
- `year` (INTEGER) - Payment year
- `sheet_name` (VARCHAR) - Source Excel sheet

## Usage

1. **Select Alley**: Choose an alley from the available options
2. **Select House**: Click on a house to view its resident's payment history
3. **View Payments**: See all payments made by the selected resident
4. **Navigate Back**: Use the "Back to Selection" button to return to the house selection

## Payment Types

The application categorizes payments by type with color coding:

- **Membership Fee** (Blue) - Annual membership fees
- **Annual Fee** (Green) - Yearly fees by year
- **Guard Fee** (Purple) - Monthly guard fees
- **Excess Payment** (Orange) - Excess payments carried forward

## Development

### Project Structure

```
src/
├── components/
│   ├── ResidentSelector.jsx    # Alley and house selection
│   └── PaymentHistory.jsx      # Payment history display
├── lib/
│   └── supabase.js            # Supabase client configuration
├── App.jsx                    # Main application component
└── index.css                  # Global styles with Tailwind
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Deployment

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory, ready for deployment to any static hosting service.

### Environment Variables

Create a `.env` file for environment-specific configuration:

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
