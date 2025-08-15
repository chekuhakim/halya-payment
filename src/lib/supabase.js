import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://dxsjgwsaycdspfjasitz.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR4c2pnd3NheWNkc3BmanNpdHoiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTczNDk5NzQ5MCwiZXhwIjoyMDUwNTczNDkwfQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)


