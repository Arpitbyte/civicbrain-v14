import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from civicbrain.infra.config import settings

async def main():
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.connect() as conn:
        res = await conn.execute(text(
            "SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid "
            "WHERE typname = 'staff_role_enum' ORDER BY enumsortorder"
        ))
        rows = res.fetchall()
        print("=== LITERAL staff_role_enum LABELS ===")
        for r in rows:
            print(r[0])
            
        res_pol = await conn.execute(text(
            "SELECT tablename, policyname, cmd, qual, with_check FROM pg_policies "
            "WHERE tablename = 'dispatch_conflict_review'"
        ))
        pols = res_pol.fetchall()
        print("\n=== LITERAL POLICIES ON dispatch_conflict_review ===")
        for p in pols:
            print(f"Table: {p[0]} | Policy: {p[1]} | Cmd: {p[2]}")
            print(f"  Qual: {p[3]}")
            print(f"  With Check: {p[4]}")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
