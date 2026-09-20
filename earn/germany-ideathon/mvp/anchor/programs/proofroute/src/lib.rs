use anchor_lang::prelude::*;

declare_id!("Fg6PaFpoGXkYsidMpWxTWqkZ2nJsHnVQyHhE8uYpJL1w");

#[program]
pub mod proofroute {
    use super::*;

    pub fn create_intent(ctx: Context<CreateIntent>, p: CreateIntentParams) -> Result<()> {
        require!(p.max_input > 0 && p.min_output > 0, ProofRouteError::InvalidBounds);
        require!(p.expiry_slot > Clock::get()?.slot, ProofRouteError::Expired);
        require!(p.intent_id.len() <= 64 && p.route_id.len() <= 64, ProofRouteError::StringTooLong);
        let i = &mut ctx.accounts.intent;
        i.proposer = ctx.accounts.proposer.key();
        i.input_mint = p.input_mint;
        i.output_mint = p.output_mint;
        i.max_input = p.max_input;
        i.min_output = p.min_output;
        i.expiry_slot = p.expiry_slot;
        i.intent_id = p.intent_id;
        i.route_id = p.route_id;
        i.evidence_hash = p.evidence_hash;
        i.authorized = false;
        i.verified_output = 0;
        i.bump = 0;
        Ok(())
    }

    pub fn attest_intent(
        ctx: Context<AttestIntent>,
        reproduced_output: u64,
        evidence_hash: [u8; 32],
    ) -> Result<()> {
        let slot = Clock::get()?.slot;
        let i = &ctx.accounts.intent;
        require!(slot <= i.expiry_slot, ProofRouteError::Expired);
        require!(evidence_hash == i.evidence_hash, ProofRouteError::EvidenceMismatch);
        require!(reproduced_output >= i.min_output, ProofRouteError::BelowMinOutput);
        let v = &mut ctx.accounts.verification;
        v.intent = i.key();
        v.verifier = ctx.accounts.verifier.key();
        v.reproduced_output = reproduced_output;
        v.evidence_hash = evidence_hash;
        v.observed_slot = slot;
        v.passed = true;
        Ok(())
    }

    pub fn authorize_intent(ctx: Context<AuthorizeIntent>) -> Result<()> {
        let slot = Clock::get()?.slot;
        let i = &mut ctx.accounts.intent;
        require_keys_eq!(i.proposer, ctx.accounts.authorizer.key(), ProofRouteError::Unauthorized);
        require!(slot <= i.expiry_slot, ProofRouteError::Expired);

        let a = &ctx.accounts.verification_a;
        let b = &ctx.accounts.verification_b;
        require_keys_eq!(a.intent, i.key(), ProofRouteError::WrongIntent);
        require_keys_eq!(b.intent, i.key(), ProofRouteError::WrongIntent);
        require!(a.verifier != b.verifier, ProofRouteError::DuplicateVerifier);
        require!(a.passed && b.passed, ProofRouteError::QuorumNotMet);
        require!(a.evidence_hash == i.evidence_hash && b.evidence_hash == i.evidence_hash,
                 ProofRouteError::EvidenceMismatch);

        let low = a.reproduced_output.min(b.reproduced_output);
        let high = a.reproduced_output.max(b.reproduced_output);
        let mid = ((a.reproduced_output as u128 + b.reproduced_output as u128) / 2) as u64;
        require!(mid >= i.min_output, ProofRouteError::BelowMinOutput);
        let spread_bps = ((high - low) as u128 * 10_000u128) / (mid as u128);
        require!(spread_bps <= 25, ProofRouteError::VerifierDisagreement);

        i.authorized = true;
        i.verified_output = mid;
        Ok(())
    }

    pub fn settle_intent(
        ctx: Context<SettleIntent>,
        actual_input: u64,
        actual_output: u64,
        fee_paid: u64,
    ) -> Result<()> {
        let slot = Clock::get()?.slot;
        let i = &mut ctx.accounts.intent;
        require!(i.authorized, ProofRouteError::NotAuthorized);
        require!(slot <= i.expiry_slot, ProofRouteError::Expired);
        require!(actual_input <= i.max_input, ProofRouteError::InputTooHigh);
        require!(actual_output >= i.min_output, ProofRouteError::BelowMinOutput);

        let r = &mut ctx.accounts.receipt;
        r.intent = i.key();
        r.executor = ctx.accounts.executor.key();
        r.actual_input = actual_input;
        r.actual_output = actual_output;
        r.fee_paid = fee_paid;
        r.settled_slot = slot;
        r.expected_output = i.verified_output;
        i.authorized = false;
        Ok(())
    }
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct CreateIntentParams {
    pub intent_id: String,
    pub input_mint: Pubkey,
    pub output_mint: Pubkey,
    pub max_input: u64,
    pub min_output: u64,
    pub expiry_slot: u64,
    pub route_id: String,
    pub evidence_hash: [u8; 32],
}

#[derive(Accounts)]
pub struct CreateIntent<'info> {
    #[account(init, payer = proposer, space = 8 + IntentAccount::INIT_SPACE)]
    pub intent: Account<'info, IntentAccount>,
    #[account(mut)]
    pub proposer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct AttestIntent<'info> {
    pub intent: Account<'info, IntentAccount>,
    #[account(init, payer = verifier, space = 8 + VerificationAccount::INIT_SPACE)]
    pub verification: Account<'info, VerificationAccount>,
    #[account(mut)]
    pub verifier: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct AuthorizeIntent<'info> {
    #[account(mut)]
    pub intent: Account<'info, IntentAccount>,
    pub verification_a: Account<'info, VerificationAccount>,
    pub verification_b: Account<'info, VerificationAccount>,
    pub authorizer: Signer<'info>,
}

#[derive(Accounts)]
pub struct SettleIntent<'info> {
    #[account(mut)]
    pub intent: Account<'info, IntentAccount>,
    #[account(init, payer = executor, space = 8 + ExecutionReceipt::INIT_SPACE)]
    pub receipt: Account<'info, ExecutionReceipt>,
    #[account(mut)]
    pub executor: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
#[derive(InitSpace)]
pub struct IntentAccount {
    pub proposer: Pubkey,
    pub input_mint: Pubkey,
    pub output_mint: Pubkey,
    pub max_input: u64,
    pub min_output: u64,
    pub expiry_slot: u64,
    #[max_len(64)]
    pub intent_id: String,
    #[max_len(64)]
    pub route_id: String,
    pub evidence_hash: [u8; 32],
    pub authorized: bool,
    pub verified_output: u64,
    pub bump: u8,
}

#[account]
#[derive(InitSpace)]
pub struct VerificationAccount {
    pub intent: Pubkey,
    pub verifier: Pubkey,
    pub reproduced_output: u64,
    pub evidence_hash: [u8; 32],
    pub observed_slot: u64,
    pub passed: bool,
}

#[account]
#[derive(InitSpace)]
pub struct ExecutionReceipt {
    pub intent: Pubkey,
    pub executor: Pubkey,
    pub actual_input: u64,
    pub actual_output: u64,
    pub fee_paid: u64,
    pub settled_slot: u64,
    pub expected_output: u64,
}

#[error_code]
pub enum ProofRouteError {
    #[msg("invalid intent bounds")] InvalidBounds,
    #[msg("intent expired")] Expired,
    #[msg("string too long")] StringTooLong,
    #[msg("evidence hash mismatch")] EvidenceMismatch,
    #[msg("reproduced or actual output below minimum")] BelowMinOutput,
    #[msg("wrong intent")] WrongIntent,
    #[msg("duplicate verifier")] DuplicateVerifier,
    #[msg("verifier quorum not met")] QuorumNotMet,
    #[msg("verifier outputs disagree beyond policy")] VerifierDisagreement,
    #[msg("not authorized")] NotAuthorized,
    #[msg("actual input exceeds max input")] InputTooHigh,
    #[msg("unauthorized authorizer")] Unauthorized,
}
