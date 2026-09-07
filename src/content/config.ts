import { defineCollection, z } from 'astro:content'

// ─── Blog ────────────────────────────────────────────────────────────────────
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title:       z.string(),
    description: z.string(),
    publishDate: z.date(),
    tags:        z.array(z.string()).default([]),
    draft:       z.boolean().default(false),
    coverImage:  z.string().optional(),
  }),
})

// ─── Whisky Journal ──────────────────────────────────────────────────────────
const whisky = defineCollection({
  type: 'content',
  schema: z.object({
    name:        z.string(),              // e.g. "Glenfarclas 12"
    distillery:  z.string(),
    region:      z.string(),             // e.g. "Speyside", "Islay"
    age:         z.number().optional(),  // age statement in years
    abv:         z.number(),             // e.g. 43.0
    rating:      z.number().min(0).max(10),
    nose:        z.string().optional(),
    palate:      z.string().optional(),
    finish:      z.string().optional(),
    tastedDate:  z.date(),
    bottleImage: z.string().optional(),
  }),
})

// ─── Photography ─────────────────────────────────────────────────────────────
const photography = defineCollection({
  type: 'content',
  schema: z.object({
    title:       z.string(),
    description: z.string().optional(),
    location:    z.string().optional(),
    takenDate:   z.date(),
    category:    z.enum(['street', 'travel', 'nature', 'family', 'portrait', 'other']),
    tags:        z.array(z.string()).default([]),
    coverImage:  z.string(),             // path in /public
    camera:      z.string().optional(),
    featured:    z.boolean().default(false),
  }),
})

export const collections = { blog, whisky, photography }
